import commands
 
def get_cpu_temp():
    tempFile = open( "/sys/class/thermal/thermal_zone0/temp" )
    cpu_temp = tempFile.read()
    tempFile.close()
    return float(cpu_temp)/1000
    # Uncomment the next line if you want the temp in Fahrenheit
    #return float(1.8*cpu_temp)+32
 
def get_gpu_temp():
    gpu_temp = commands.getoutput( '/opt/vc/bin/vcgencmd measure_temp' ).replace( 'temp=', '' ).replace( '\'C', '' )
    return  float(gpu_temp)
    # Uncomment the next line if you want the temp in Fahrenheit
    # return float(1.8* gpu_temp)+32

def average_temp():
   cpu = get_cpu_temp()
   gpu = get_gpu_temp()
   average = cpu + gpu
   average = average / 2
   return float(average)

def percentage_max():
   max = 80
   average = average_temp()
   percent = average / max
   percent = percent * 100
   return int(percent)
 
def main():
    print "CPU temp: ", str(get_cpu_temp())
    print "GPU temp: ", str(get_gpu_temp())
    print "(" + str(percentage_max()) + "% of maximum)"
if __name__ == '__main__':
    main()
