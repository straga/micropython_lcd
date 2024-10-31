set(IDF_TARGET esp32s3)

set(SDKCONFIG_DEFAULTS
    
    ${SDKCONFIG_IDF_VERSION_SPECIFIC}               #esp-idf version specific
    boards/sdkconfig.base                           #base
    boards/sdkconfig.usb                            #usb
    boards/sdkconfig.ble                            #ble
    boards/sdkconfig.spiram_sx                      #spiram 
    # spiram octa
    boards/sdkconfig.240mhz
    boards/sdkconfig.spiram_oct
                 
    boards/STRAGA/sdkconfig.board                   #board default
    boards/STRAGA_S3_SPIRAM_LCD/sdkconfig.board     #board specific
)

set(MICROPY_FROZEN_MANIFEST ${MICROPY_BOARD_DIR}/manifest.py)

