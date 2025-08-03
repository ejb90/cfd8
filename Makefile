# cloneandbuild:
# 	mkdir build

# 	git clone https://github.com/KarypisLab/GKlib.git build/GKlib
# 	$(MAKE) -C build/GKlib config cc=gcc
# 	$(MAKE) -C build/GKlib install

# 	git clone https://github.com/KarypisLab/METIS.git build/METIS
# 	cd build/METIS && $(MAKE) config "cc=gcc" && $(MAKE) install

# 	git clone https://github.com/KarypisLab/ParMETIS.git build/ParMETIS
# 	$(MAKE) -C build/ParMETIS config cc=mpicc
# 	$(MAKE) -C build/ParMETIS install

# 	# git clone git@github.com:ucns3d-team/UCNS3D.git
# 	git clone git@github.com:ejb90/UCNS3D.git -b s421784
# 	cd UCNS3D/src && ln -sf ../../GKlib/build/Linux-x86_64/libGKlib.a
# 	cd UCNS3D/src && ln -sf ../../METIS/build/libmetis/libmetis.a
# 	cd UCNS3D/src && ln -sf ../../ParMETIS/build/Linux-x86_64/libparmetis/libparmetis.a
# 	cd UCNS3D/src && ln -sf ../bin/lib/tecplot/libtecio.a
# 	cd UCNS3D/src && ln -s ../bin/gnu-compiler/Makefile Makefile
# 	cd UCNS3D/src && $(MAKE) -f ../bin/gnu-compiler/Makefile clean all


MAKEFILE_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))


deps:
	bash $(MAKEFILE_DIR)local.bash

exe: build/UCNS3D/src/ucns3d_p
	cd build/UCNS3D/src && \
	make -f ../bin/gnu-compiler/Makefile ucns3d_p

.PHONY: deps exe






# # Makefile converted from local.bash
# # Variables
# CC = gcc
# MPICC = mpicc
# BUILD_DIR = build

# # Default target
# all: setup gklib metis parmetis ucns3d

# # Create build directory and setup
# setup:
# 	mkdir -p $(BUILD_DIR)

# # Build GKlib
# gklib: setup
# 	cd $(BUILD_DIR) && \
# 	if [ ! -d "GKlib" ]; then git clone https://github.com/KarypisLab/GKlib.git; fi && \
# 	cd GKlib && \
# 	make config cc=$(CC) && \
# 	make install

# # Build METIS
# metis: setup
# 	cd $(BUILD_DIR) && \
# 	if [ ! -d "METIS" ]; then git clone https://github.com/KarypisLab/METIS.git; fi && \
# 	cd METIS && \
# 	make config cc=$(CC) && \
# 	make install

# # Build ParMETIS
# parmetis: setup
# 	cd $(BUILD_DIR) && \
# 	if [ ! -d "ParMETIS" ]; then git clone https://github.com/KarypisLab/ParMETIS.git; fi && \
# 	cd ParMETIS && \
# 	make config cc=$(MPICC) && \
# 	make install

# # Clone and build UCNS3D
# ucns3d: gklib metis parmetis
# 	cd $(BUILD_DIR) && \
# 	if [ ! -d "UCNS3D" ]; then git clone git@github.com:ejb90/UCNS3D.git -b s421784; fi && \
# 	cd UCNS3D/src && \
# 	ln -sf ../../GKlib/build/Linux-x86_64/libGKlib.a . && \
# 	ln -sf ../../METIS/build/libmetis/libmetis.a . && \
# 	ln -sf ../../ParMETIS/build/Linux-x86_64/libparmetis/libparmetis.a . && \
# 	ln -sf ../bin/lib/tecplot/libtecio.a . && \
# 	ln -sf ../bin/gnu-compiler/Makefile . && \
# 	make -f ../bin/gnu-compiler/Makefile clean all

# # Clean targets
# clean:
# 	rm -rf $(BUILD_DIR)

# clean-gklib:
# 	if [ -d "$(BUILD_DIR)/GKlib" ]; then cd $(BUILD_DIR)/GKlib && make clean; fi

# clean-metis:
# 	if [ -d "$(BUILD_DIR)/METIS" ]; then cd $(BUILD_DIR)/METIS && make clean; fi

# clean-parmetis:
# 	if [ -d "$(BUILD_DIR)/ParMETIS" ]; then cd $(BUILD_DIR)/ParMETIS && make clean; fi

# clean-ucns3d:
# 	if [ -d "$(BUILD_DIR)/UCNS3D/src" ]; then cd $(BUILD_DIR)/UCNS3D/src && make -f ../bin/gnu-compiler/Makefile clean; fi

# # Force rebuild targets
# rebuild-gklib: clean-gklib gklib

# rebuild-metis: clean-metis metis

# rebuild-parmetis: clean-parmetis parmetis

# rebuild-ucns3d: clean-ucns3d ucns3d

# rebuild-all: clean all

# # Phony targets
# .PHONY: all setup clean clean-gklib clean-metis clean-parmetis clean-ucns3d
# .PHONY: gklib metis parmetis ucns3d
# .PHONY: rebuild-gklib rebuild-metis rebuild-parmetis rebuild-ucns3d rebuild-all