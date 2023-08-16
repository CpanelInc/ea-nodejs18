OBS_PROJECT := EA4
OBS_PACKAGE := ea-nodejs18
DISABLE_BUILD = repository=CentOS_6.5_standard repository=CentOS_7
include $(EATOOLS_BUILD_DIR)obs.mk
