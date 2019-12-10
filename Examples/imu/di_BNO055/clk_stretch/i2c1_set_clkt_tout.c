#include<stdio.h>
#include<stdint.h>
#include<stdlib.h>
#include<fcntl.h>
#include<sys/mman.h>
#include<unistd.h>
#include<errno.h>


#define MODULE_NAME		"i2c1_set_clkt_tout"

//#define BCM2708_PERI_BASE (0x20000000)
//#define I2C1_BASE (BCM2708_PERI_BASE + 0x00804000)
#define I2C1_BASE (0x3f804000)
//#define I2C1_CLKT (I2C1_BASE + 0x1C)
#define BLOCK_SIZE (4*8)

enum {
	ERR_CODE_SUCCESS,
	ERR_CODE_BAD_PARAM_COUNT,
	ERR_CODE_BAD_PARAM_VALUE,
	ERR_CODE_DRIVER_OPEN,
	ERR_CODE_MMAP,
	ERR_CODE_MUNMAP,
};

typedef struct {
	uint32_t C;
	uint32_t S;
	uint32_t DLEN;
	uint32_t A;
	uint32_t FIFO;
	uint32_t DIV;
	uint32_t DEL;
	uint32_t CLKT;
} i2c_reg_map_t;


void log_message(char *str) {
	printf("%s: %s\n", MODULE_NAME, str);
}

int main(int argc, char *argv[]) {
	char buffer[100];
	int file_ref;
	void *map;
	i2c_reg_map_t *i2c_reg_map;
	int tout;

	if(argc != 2) {
		return ERR_CODE_BAD_PARAM_COUNT;
	}
	
	tout = atoi(argv[1]);
	
	if((tout <= 0) || (tout > 65535)) {
		return ERR_CODE_BAD_PARAM_VALUE;
	}

	if((file_ref = open("/dev/mem", O_RDWR | O_SYNC)) == -1) {
		log_message("driver open FAILED");
		return ERR_CODE_DRIVER_OPEN;
	}

	map = mmap(	NULL, //auto choose address
			BLOCK_SIZE, //map length
			PROT_READ | PROT_WRITE, //enable read, write
			MAP_SHARED, //shared with other process
			file_ref, // file reference
			I2C1_BASE // offset to I2C1
	);

	if(map == MAP_FAILED) {
		log_message("mmap FAILED");
		return ERR_CODE_MMAP;
	}

	i2c_reg_map = (i2c_reg_map_t *)map;

	i2c_reg_map->CLKT = tout;
	//sprintf(buffer, "CLKT.TOUT = 0x%.8X", i2c_reg_map->CLKT);
	sprintf(buffer, "CLKT.TOUT = %d", i2c_reg_map->CLKT);
	log_message(buffer);
	
    // Don't forget to free the mmapped memory
    if (munmap(map, BLOCK_SIZE) == -1) {
		log_message("munmap FAILED");
		return ERR_CODE_MUNMAP;
    }

    // Un-mmaping doesn't close the file, so we still need to do that
    close(file_ref);
	
	return ERR_CODE_SUCCESS;
}
