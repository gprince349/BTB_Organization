#include "pdede.h"

#if defined(PDEDEBTB)

map<uint64_t, set<uint64_t>> btb_unique_addr;
map<uint64_t, uint64_t> btb_fill_count;

void RAS::push(uint64_t ret_addr, uint64_t call_addr, uint64_t target,
               uint64_t bb_size) {
  if (head >= MAX_RAS_DEPTH - 1) {
    max_depth_exceeded_cnt++;
    return;
  }
  head++;

  return_address[head] = ret_addr;
  target_address[head] = target;
  caller_trigger[head] = call_addr;
}

void RAS::pop() {
  if (head < 0) {
    return;
  }
  --head;
}

uint64_t PDEDE_BTB::get_tag(uint64_t addr, uint8_t btb_type) {
  addr >>= 2;
  if (btb_type == IS_L1BTB) {
    addr >>= LOG2_L1BTB_SET;
    return addr;
  } else if (btb_type == IS_L2BTB) {
    addr = addr & ((1L << L2BTB_PARTIAL_TAG_BITS) - 1);
    return addr;
  } else
    assert(0);
}

uint64_t PDEDE_BTB::get_target(uint64_t addr, uint8_t btb_type) {
  if (btb_type == IS_L1BTB) {
    return addr;
  } else if (btb_type == IS_L2BTB) // Partial target
  {
    addr = addr & ((1L << L2BTB_PARTIAL_TARGET_BITS) - 1);
    return addr;
  } else {
    assert(0);
  }
}

uint32_t PDEDE_BTB::find_victim(uint8_t btb_type, uint64_t addr) {
  uint32_t set = get_set(addr, btb_type);
  CACHE &BTB = btb_type == IS_L1BTB ? L1BTB : L2BTB;

  for (int way = 0; way < BTB.NUM_WAY; way++)
    if (BTB.block[set][way].valid == false)
      return way;

  for (int way = 0; way < BTB.NUM_WAY; way++)
    if (BTB.block[set][way].lru == BTB.NUM_WAY - 1)
      return way;

  cerr << btb_type << " BTB No victim found! " << endl;
  assert(0);
}

void PDEDE_BTB::update_replacement_state(uint8_t btb_type, uint32_t set,
                                            uint32_t way) {
  CACHE &BTB = btb_type == IS_L1BTB ? L1BTB : L2BTB;

  for (int i = 0; i < BTB.NUM_WAY; i++) {
    if (BTB.block[set][i].lru < BTB.block[set][way].lru) {
      BTB.block[set][i].lru++;
    }
  }
  BTB.block[set][way].lru = 0;
}

uint32_t PDEDE_BTB::get_set(uint64_t address, uint8_t btb_type) {
  address >>= 2;
  if (btb_type == IS_L1BTB) {
    return (uint32_t)(address & ((1L << LOG2_L1BTB_SET) - 1));
  } else if (btb_type == IS_L2BTB) {
    uint32_t lower_14_bits = address & ((1L << 14) - 1);
    address >>= 14;
    uint32_t next_14_bits = address & ((1L << 14) - 1);
    next_14_bits ^= lower_14_bits;
    return (next_14_bits & ((1L << LOG2_L2BTB_SET) - 1));
  } else
    assert(0);
}

uint32_t PDEDE_BTB::get_way(uint64_t addr, uint32_t set, uint8_t btb_type) {
  CACHE &BTB = btb_type == IS_L1BTB ? L1BTB : L2BTB;

  for (uint32_t way = 0; way < BTB.NUM_WAY; way++) {
    if (BTB.block[set][way].valid &&
        BTB.block[set][way].tag == get_tag(addr, btb_type))
      return way;
  }

  if (btb_type == IS_L1BTB)
    return L1BTB_WAY;
  else
    return L2BTB_WAY;
}

uint32_t PDEDE_BTB::fill_btb(uint64_t trigger, uint64_t target,
                                uint8_t branch_type, uint8_t btb_type) {
  if (btb_type == IS_L1BTB || btb_type == IS_BTB_BOTH) {
    uint32_t set = get_set(trigger, IS_L1BTB);
    uint32_t way = get_way(trigger, set, IS_L1BTB);

    if (way == L1BTB_WAY) {
      way = find_victim(IS_L1BTB, trigger);
    }

    update_replacement_state(IS_L1BTB, set, way);

    L1BTB.block[set][way].valid = true;
    L1BTB.block[set][way].tag = get_tag(trigger, IS_L1BTB);

    //implementing target encoding
    if ((target >> OFFSET_BIT) == (trigger >> OFFSET_BIT)){
        // cout<<"PC: "<<trigger<<" target: "<<target<<" first 45 bit: "<<((target >> OFFSET_BIT))<<endl;
        //here only set delta bit to one and store offset only
        uint64_t offset = target & ((1L << OFFSET_BIT) -1);
        L1BTB.block[set][way].delta_bit = 1;
        L1BTB.block[set][way].data = offset;
    }
    else{

        //this part for pdede target partitioning 
        //target data update in partitioned fashion   data is 64 bit here so we split it in three part 
        // first pointer to region  -> require LOG2_NUM_REGION bits
        //second page bit 16  -> require LOG2_NUM_PAGE bits
        //third offset  19
        //  so find these all three and concat and put in data

        // L1BTB.block[set][way].data = get_target(target, IS_L1BTB);
        uint64_t region_index = find_victim_region(target);
        uint64_t page_index = find_victim_page(target);
        uint64_t offset = target & ((1L << OFFSET_BIT) -1);
        
        uint64_t data = combine_pg_reg_offset(region_index,page_index,offset);

        L1BTB.block[set][way].delta_bit = 0;
        L1BTB.block[set][way].data = data;

        }
  }

  if (btb_type == IS_L2BTB || btb_type == IS_BTB_BOTH) {
    uint32_t set = get_set(trigger, IS_L2BTB);
    uint32_t way = get_way(trigger, set, IS_L2BTB);

    if (way == L2BTB_WAY) {
      way = find_victim(IS_L2BTB, trigger);
    }

    btb_fill_count[set]++;
    btb_unique_addr[set].insert(trigger);

    update_replacement_state(IS_L2BTB, set, way);

    L2BTB.block[set][way].valid = true;
    L2BTB.block[set][way].tag = get_tag(trigger, IS_L2BTB);
    L2BTB.block[set][way].data = get_target(target, IS_L2BTB);
  }
}


//finding whether target data's region already there or not (incase find a victim if not there and update region data and replacement policy)
//if already there just return index and update replacement policy

uint64_t PDEDE_BTB::find_victim_region(uint64_t target){

            uint64_t region_data =  (target >> (PAGE_BIT+OFFSET_BIT));

            // cout<<"region-  data --"<<region_data<<endl;
            
            uint64_t index = NUM_REGION;

            for(int i =0; i<NUM_REGION; i++){
                if(region[i].data == region_data){
                    index = i;
                    break;
                }
            }

            if (index == NUM_REGION){//index == MAX so this region was not available so add one
                int max = 0;
                for(int i =0; i<NUM_REGION; i++){
                    if (region[i].srrip >= max){
                        max = region[i].srrip;
                        index = i;
                    }
                }
                //got the index now we'll replace the data
                region[index].data = region_data;

            }

            //updating replacement policy bits

            for(int i =0; i<NUM_REGION; i++){
                    if(region[i].srrip <= region[index].srrip){
                        region[i].srrip++;
                        // cout<<"region -less --"<<region[i].srrip<<endl;
                    }
                }

            region[index].srrip =0;

            // cout<<"region index-> "<<index<<endl;
            return index; 
}


//finding whether target data's page already there or not (incase find a victim if not there and update page data and replacement policy)
//if already there just return index and update replacement policy
uint64_t PDEDE_BTB::find_victim_page(uint64_t target){

                uint64_t page_data = (target >> OFFSET_BIT) & ((1L << PAGE_BIT)-1);

                //  cout<<"page -- data --> "<<page_data<<endl;

                uint64_t index = NUM_PAGE;
                for(int i =0; i<NUM_PAGE; i++){
                    if(page[i].data == page_data){
                        index = i;
                        break;
                    }
                }

                if (index == NUM_PAGE){//index == -1 so this page was not available so add one
                    int max = 0;
                    for(int i =0; i<NUM_PAGE; i++){
                        if (page[i].srrip >= max){
                            max = page[i].srrip;
                            index = i;
                        }
                    }
                    //got the index now we'll replace the data
                    page[index].data = page_data;

                }

                //updating replacement policy bits
                for(int i =0; i<NUM_PAGE; i++){
                        if(page[i].srrip <= page[index].srrip){
                            page[i].srrip++;
                        }
                    }

                page[index].srrip =0;

                // cout<<"page index-->"<<index<<endl;
                return index;
}


//combining the pointers to page and region along with offset to store in BTB monitor
uint64_t PDEDE_BTB::combine_pg_reg_offset(uint64_t region_index, uint64_t page_index, uint64_t offset){

         return   (region_index << (OFFSET_BIT + LOG2_NUM_PAGE)) + (page_index << OFFSET_BIT) + offset;
}


uint64_t PDEDE_BTB::reconstruct_target_data(uint64_t address, uint64_t set, uint64_t way){

        if(L1BTB.block[set][way].delta_bit == 1){
            //target encoding part
            uint64_t data = L1BTB.block[set][way].data;
            uint64_t offset = data & ((1L << OFFSET_BIT)-1);
            return ((address >> OFFSET_BIT) << OFFSET_BIT ) + offset;
        }
        else{

            //this data contains pointer to region, page and offset
            uint64_t data = L1BTB.block[set][way].data;

            uint64_t offset = data & ((1L << OFFSET_BIT)-1);
            data = data >> OFFSET_BIT;
            uint64_t page_index = data & ((1L << LOG2_NUM_PAGE) -1);
            data = data >> LOG2_NUM_PAGE;
            uint64_t region_index = data;


            uint64_t target = (region[region_index].data << (PAGE_BIT + OFFSET_BIT));
            target += (page[page_index].data << OFFSET_BIT);
            target += offset;

            // cout<<"target-->"<<target<<endl;
            return target;
        }
}


#endif
