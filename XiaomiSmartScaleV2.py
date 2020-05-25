'''
Created on May 2020

Contributor :
- Agung Pambudi <agung.pambudi5595@gmail.com>
- Azman Latif <azman.latif@mail.ugm.ac.id>
'''

import pygatt
from XiaomiSmartScaleBodyMetrics import bodyMetrics

#import logging
#logging.basicConfig()
#logging.getLogger('pygatt').setLevel(logging.DEBUG)

def handleData(handle, value):
    if len(value) == 13:
        emptyLoad = value[1] & (1<<7)
        isStabilized = value[1] & (1<<5)
        hasImpedance = value[1] & (1<<1)
        impedance = ((value[10] & 0xFF) << 8) | (value[9] & 0xFF)
        weight = (((value[12] & 0xFF) << 8) | (value[11] & 0xFF)) / 200.0

        if emptyLoad:
            print('Empty load')
        else:
            print('Weight {} kg'.format(weight))    

        if isStabilized:
            print('Stabilized')

        if hasImpedance:
            height = 175
            age = 25
            sex = 'men'

            lib = bodyMetrics(weight, height, age, sex, impedance)
            
            print('LBM = {}'.format(lib.getLBMCoefficient()))
            print('Body fat = {}'.format(lib.getFatPercentage()))
            print('Body fat scale = {}'.format(lib.getFatPercentageScale()))
            print('Water = {}'.format(lib.getWaterPercentage()))
            print('Water scale = {}'.format(lib.getWaterPercentageScale()))
            print('Bone mass = {}'.format(lib.getBoneMass()))
            print('Bone mass scale = {}'.format(lib.getBoneMassScale()))
            print('Muscle mass = {}'.format(lib.getMuscleMass()))
            print('Muscle mass scale = {}'.format(lib.getMuscleMassScale()))
            print('Visceral fat = {}'.format(lib.getVisceralFat()))
            print('Visceral fat scale = {}'.format(lib.getVisceralFatScale()))
            print('BMI = {}'.format(lib.getBMI()))
            print('BMI scale = {}'.format(lib.getBMIScale()))
            print('BMR = {}'.format(lib.getBMR()))
            print('BMR scale = {}'.format(lib.getBMRScale()))
            print('Ideal weight = {}'.format(lib.getIdealWeight()))

try:
    adapter = pygatt.GATTToolBackend(hci_device='hci0')
    adapter.start()

    for discover in adapter.scan(run_as_root=True, timeout=5):
        if discover['name'] == 'MIBFS':
            try:
                print('Device found, try to connect with device')
                device = adapter.connect(discover['address'])
                print('Connected with device')
                                
                while True:
                    device.subscribe('00002a9c-0000-1000-8000-00805f9b34fb', callback=handleData)

            except KeyboardInterrupt:
                print('Terminate')
            except:
                print('Failed to connect with device')
            finally:
                device.disconnect()
                
except KeyboardInterrupt:
    print('Terminate')
except:
    print('Something went wrong with adapter')
finally:
    adapter.stop()