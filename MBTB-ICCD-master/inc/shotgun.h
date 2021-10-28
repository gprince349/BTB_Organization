/*
SHOTGUN BTB class methods declared here.
*/

#include "champsim.h"
#include "instruction.h"
#include <bits/stdc++.h>
#include <iostream>
#include <iterator> // for iterators
#include <unordered_map>
#include <vector>

#if defined(SHOTGUN_BTB)

using namespace std;

#define L1I_SET 64 // define this here

#if defined(SKEWED_SHOTGUN_BTB)
#define UBTB_SET 2048 // 4096 //512
#define UBTB_WAY 1    // 6 //3
#define LOG2_UBTB_SET (int)(ceil(log2(UBTB_SET)))
#define LOG2_UBTB_WAY 1 //(int)(ceil(log2(UBTB_WAY)))

#define CBTB_SET 1024 // 512 //128 //64 //32
#define CBTB_WAY 1    // 4
#define LOG2_CBTB_SET (int)(ceil(log2(CBTB_SET)))
#define LOG2_CBTB_WAY 1 //(int)(ceil(log2(CBTB_WAY)))

#define RIB_SET 1024 // 256 //128
#define RIB_WAY 1    // 4
#define LOG2_RIB_SET (int)(ceil(log2(RIB_SET)))
#define LOG2_RIB_WAY 1 //(int)(ceil(log2(RIB_WAY)))

#else

#define UBTB_SET 1024
#define UBTB_WAY 4
#define LOG2_UBTB_SET (int)(ceil(log2(UBTB_SET)))
#define LOG2_UBTB_WAY (int)(ceil(log2(UBTB_WAY)))

#define CBTB_SET 512
#define CBTB_WAY 4
#define LOG2_CBTB_SET (int)(ceil(log2(CBTB_SET)))
#define LOG2_CBTB_WAY (int)(ceil(log2(CBTB_WAY)))

#define RIB_SET 512
#define RIB_WAY 4
#define LOG2_RIB_SET (int)(ceil(log2(RIB_SET)))
#define LOG2_RIB_WAY (int)(ceil(log2(RIB_WAY)))

#endif

#define LOG2_INSTR_SIZE 2
#define IP_SIZE 64
#define TARGET (IP_SIZE - LOG2_INSTR_SIZE)

#define SHOTGUN_ACCESS_LATENCY 2

#if defined(SKEWED_SHOTGUN_BTB)
#define UBTB_TAG                                                               \
  (IP_SIZE - LOG2_INSTR_SIZE) //((IP_SIZE - LOG2_INSTR_SIZE) - LOG2_UBTB_SET)
#define CBTB_TAG                                                               \
  (IP_SIZE - LOG2_INSTR_SIZE) //((IP_SIZE - LOG2_INSTR_SIZE) - LOG2_CBTB_SET)
#define RIB_TAG                                                                \
  (IP_SIZE - LOG2_INSTR_SIZE) //((IP_SIZE - LOG2_INSTR_SIZE) - LOG2_RIB_SET)
#else
#define UBTB_TAG ((IP_SIZE - LOG2_INSTR_SIZE) - LOG2_UBTB_SET)
#define CBTB_TAG ((IP_SIZE - LOG2_INSTR_SIZE) - LOG2_CBTB_SET)
#define RIB_TAG ((IP_SIZE - LOG2_INSTR_SIZE) - LOG2_RIB_SET)
#endif

#define BB_SIZE 5

#define SPACIAL_FOOTPRINT_PREV 2
#define SPACIAL_FOOTPRINT_FWD 6
#define SPACIAL_FOOTPRINT (SPACIAL_FOOTPRINT_PREV + SPACIAL_FOOTPRINT_FWD)

// assert ((ceil(log2(SPACIAL_FOOTPRINT))) <= BB_SIZE);

#define CALLER_FOOTPRINT 0
#define RETURN_FOOTPRINT 1

#define UNCONDITIONAL 2
#define CALL 1

#define IS_UBTB 1
#define IS_CBTB 2
#define IS_RIB 3

#define MAX_RAS_DEPTH 32
#define PREFETCH_BUFFER_LEN 32

#define PREDECODE_BUFFER_LEN 32
#define PREDECODE_WIDTH 6

#define MAX_WAYS(x)                                                            \
  ((x == IS_UBTB) ? UBTB_WAY : ((x == IS_CBTB) ? CBTB_WAY : RIB_WAY))

class Conds {
public:
  uint64_t ip, branch_target, branch_type;
};

class UBTB_ENTRY {
public:
  bool valid;
  bool type;
  // type 0 is unconditional jump BRANCH_DIRECT_JUMP and BRANCH_INDIRECT
  // type 1 is call BRANCH_DIRECT_CALL and BRANCH_INDIRECT_CALL
  // see UNCONDITIONAL and CALL
  bitset<LOG2_UBTB_WAY> lru;
  bitset<UBTB_TAG> tag;
  bitset<TARGET> target;
  bitset<BB_SIZE> basic_block_size;
  // basic_block_size in cache blocks over the trigger block
  bitset<SPACIAL_FOOTPRINT> call_footprint;
  bitset<SPACIAL_FOOTPRINT> return_footprint;

  UBTB_ENTRY() {
    valid = false;
    type = 0;
    lru = bitset<LOG2_UBTB_WAY>(0);
    tag = bitset<UBTB_TAG>(0);
    target = bitset<TARGET>(0);
    basic_block_size = bitset<BB_SIZE>(0);
    call_footprint = bitset<SPACIAL_FOOTPRINT>(0);
    return_footprint = bitset<SPACIAL_FOOTPRINT>(0);
  };
};

class CBTB_ENTRY {
public:
  bool valid;
  bitset<LOG2_CBTB_WAY> lru;
  bitset<CBTB_TAG> tag;
  bitset<TARGET> target;
  // TODO: We can save space if we store offset from IP rather than target.
  bitset<BB_SIZE> basic_block_size;
  // Why do we need to store 2 bits for conditional branch prediction?

  CBTB_ENTRY() {
    valid = false;
    lru = bitset<LOG2_CBTB_WAY>(0);
    tag = bitset<CBTB_TAG>(0);
    target = bitset<TARGET>(0);
    basic_block_size = bitset<BB_SIZE>(0);
  };
};

class RIB_ENTRY {
public:
  bool valid;
  bitset<LOG2_RIB_WAY> lru;
  bitset<RIB_TAG> tag;
  bitset<BB_SIZE> basic_block_size;

  RIB_ENTRY() {
    valid = false;
    lru = bitset<LOG2_RIB_WAY>(0);
    tag = bitset<RIB_TAG>(0);
    basic_block_size = bitset<BB_SIZE>(0);
  };
};

class RAS {
public:
  uint64_t return_address[MAX_RAS_DEPTH];
  uint64_t target_address[MAX_RAS_DEPTH];
  uint64_t caller_trigger[MAX_RAS_DEPTH];
  bitset<BB_SIZE> basic_block_size[MAX_RAS_DEPTH];
  int head;

  uint64_t max_depth_exceeded_cnt = 0;

  RAS() { head = -1; };

  void push(uint64_t ret_addr, uint64_t call, uint64_t target,
            uint64_t bb_size);
  void pop();
};

class PREFETCH_BUFFER_ENTRY {
public:
  bool valid;
  uint32_t lru;
  uint64_t ip;
  uint64_t target;
  uint8_t btb_type;
  bool uncond_branch_type;

  PREFETCH_BUFFER_ENTRY() {
    valid = false;
    lru = 0;
    ip = 0;
    target = 0;
    btb_type = 0;
    uncond_branch_type = 0;
  }
};

class PREDECODE_BLOCK {
public:
  uint64_t blk_addr;
  uint64_t missed_ip;
};

// Should SHOTGUN be a derived class from MEMORY?
class SHOTGUN {
public:
  string NAME = "SHOTGUN";
  uint32_t cpu;
  uint64_t curr_bb_address; // ip of call of current code region
  uint8_t curr_bb_type;
  uint32_t active_ubtb_set; // set of entry where recording happens
  uint32_t active_ubtb_way; // way of entry where recording happens
  uint8_t active_footprint; // see CALLER_FOOTPRINT and RETURN_FOOTPRINT

  uint64_t total_miss_latency = 0;

  // int fill_level; // do you need a fill level? No you don't.
  uint64_t sim_access[NUM_CPUS][NUM_TYPES], sim_hit[NUM_CPUS][NUM_TYPES],
      sim_miss[NUM_CPUS][NUM_TYPES], sim_miss_target[NUM_CPUS][NUM_TYPES],
      roi_access[NUM_CPUS][NUM_TYPES], roi_hit[NUM_CPUS][NUM_TYPES],
      roi_miss[NUM_CPUS][NUM_TYPES], roi_miss_target[NUM_CPUS][NUM_TYPES];

  vector<Conds> conditionals[L1I_SET];
  std::string condfile;

  unordered_map<uint64_t, uint64_t> basic_block_size_per_ip;
  std::string basic_block_file;

  UBTB_ENTRY **ubtb;
  CBTB_ENTRY **cbtb;
  RIB_ENTRY **rib;

  RAS ras;

  int access_latency = SHOTGUN_ACCESS_LATENCY;

  PREFETCH_BUFFER_ENTRY pbuf[PREFETCH_BUFFER_LEN];
  PREDECODE_BLOCK predecode_buffer[PREDECODE_BUFFER_LEN];
  uint32_t predecode_buffer_head;
  uint32_t predecode_buffer_tail;
  uint32_t predecode_buffer_occupancy;

  SHOTGUN() {
    predecode_buffer_head = 0;
    predecode_buffer_tail = 0;
    predecode_buffer_occupancy = 0;

    for (uint32_t i = 0; i < PREFETCH_BUFFER_LEN; ++i) {
      pbuf[i].lru = i;
    }

    ubtb = new UBTB_ENTRY *[UBTB_SET];
    for (uint32_t i = 0; i < UBTB_SET; ++i) {
      ubtb[i] = new UBTB_ENTRY[UBTB_WAY];
      for (uint32_t j = 0; j < UBTB_WAY; ++j)
        ubtb[i][j].lru = j;
    }

    cbtb = new CBTB_ENTRY *[CBTB_SET];
    for (uint32_t i = 0; i < CBTB_SET; ++i) {
      cbtb[i] = new CBTB_ENTRY[CBTB_WAY];
      for (uint32_t j = 0; j < CBTB_WAY; ++j)
        cbtb[i][j].lru = j;
    }

    for (uint32_t j = 0; j < CBTB_WAY; j++)
      cout << "Set 35: way: " << j << cbtb[35][j].lru.to_ulong() << endl;

    rib = new RIB_ENTRY *[RIB_SET];
    for (uint32_t i = 0; i < RIB_SET; ++i) {
      rib[i] = new RIB_ENTRY[RIB_WAY];
      for (uint32_t j = 0; j < RIB_WAY; ++j)
        rib[i][j].lru = j;
    }

    for (uint32_t i = 0; i < NUM_CPUS; ++i) {
      for (uint32_t j = 0; j < NUM_TYPES; ++j) {
        sim_access[i][j] = 0;
        sim_hit[i][j] = 0;
        sim_miss[i][j] = 0;
        roi_access[i][j] = 0;
        roi_hit[i][j] = 0;
        roi_miss[i][j] = 0;
      }
    }
  };

  ~SHOTGUN() {
    // for(int k=0; k<L1I_SET; ++k)
    // {
    //     printf("\n");
    //     int set = k;
    //     printf("SET %d SIZE %d\n", k, conditionals[set].size());
    //     for(int i=0; i<conditionals[set].size(); ++i)
    //         printf("ip:%x\tpa:%x\tset:%d\tcount:%d\ttarget:%x\n",
    //         (void*)(conditionals[set][i].instruction.ip),
    //         (void*)(conditionals[set][i].physical_address),
    //         sets[set][i], counts[set][i],
    //         (void*)(conditionals[set][i].instruction.branch_target));
    //
    //     printf("\n\n\n");
    // }

    // for (int s=0; s< RIB_SET; ++s)
    // {
    //     printf("\n\nSET %d", s);
    //     for (int w=0; w<RIB_WAY; ++w)
    //         printf("\nWay:%d\tValid:%d\tTag:%x", w, rib[s][w].valid,
    //         rib[s][w].tag.to_ulong());
    // }

    for (uint32_t i = 0; i < UBTB_SET; ++i)
      delete[] ubtb[i];
    delete[] ubtb;

    for (uint32_t i = 0; i < CBTB_SET; ++i)
      delete[] cbtb[i];
    delete[] cbtb;

    for (uint32_t i = 0; i < RIB_SET; ++i)
      delete[] rib[i];
    delete[] rib;
  };

  uint32_t find_victim(uint8_t btb_type, uint32_t set);
  // btb_type: see IS_UBTB, IS_CBTB and IS_RIB
  void update_replacement_state(uint8_t btb_type, uint32_t set, uint32_t way);

  // send the full IP as address
  uint32_t get_set(uint64_t address, uint8_t btb_type);
  uint32_t get_way(uint64_t address, uint32_t set, uint8_t btb_type);

  uint32_t fill_btb(uint64_t trigger, uint64_t target, uint8_t btb_type,
                    bool branch_type);
  uint32_t predecode(uint64_t address,
                     uint64_t missed_ip); // block address (6 bits shifted)
  void operate_predecode();
  void add_pf(uint64_t ip, uint64_t target, uint8_t btb_type,
              bool uncond_branch_type);
};

#endif
