include config

.PHONY: nodestart
nodestart:
	cd $(NODEDIR) ;\
	../$(FETCHAIBUILDDIR)/apps/constellation/constellation -port 8000 -block-interval 3000 -standalone

