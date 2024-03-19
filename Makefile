# Makefile for creating an executable from src/lsr.py

# Variables
PYTHON := python3
LSR_SCRIPT := src/lsr.py
DVR_SCRIPT := src/dvr.py

# Targets
.PHONY: all clean

default:
	@echo "Please specify a target."
	@false

lsr: $(LSR_SCRIPT)
	@echo "Creating executable 'lsr'..."
	printf '#!/usr/bin/env python\n' > lsr
	cat $(LSR_SCRIPT) >> lsr
	chmod +x lsr
	@echo "Executable 'lsr' created successfully."

dvr: $(DVR_SCRIPT)
	@echo "Creating executable 'dvr'..."
	printf '#!/usr/bin/env python\n' > dvr
	cat $(DVR_SCRIPT) >> dvr
	chmod +x dvr
	@echo "Executable 'dvr' created successfully."

clean:
	@rm -f lsr
	@rm -f dvr
	@echo "Cleaned up executables 'lsr' and 'dvr'."
