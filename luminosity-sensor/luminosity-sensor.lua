SID = "GVT-6780"
KEY = "3003001298"

wifi.setmode(wifi.STATION)
wifi.sta.config (SSID , KEY)
 
broker="192.168.25.178"
PORT = "1883"
seconds = 60
deviceID = "esp03"
roomID = "2"
 
humi="XX"
temp="XX"
 
mqtt_dest = {}
mqtt_valu = {}

PIN = adc.read(0) 
 -- data pin, GPIO0
-- PIN = 3 -- data pin, GPIO0
--PIN = 4 -- data pin, GPIO2
 
--load DHT22 module and read sensor
--function ReadDHT22()
--dht22 = require("dht22")
--dht22.read(PIN)
--t = dht22.getTemperature()
--h = dht22.getHumidity()
--humi=(h/10).."."..(h%10)
--temp=(t/10).."."..(t%10)
--dht22 = nil
--package.loaded["dht22"]=nil
--end
 
function mqttHandle(n)
if mqtt_dest[1] ~= nil then
print("MQTT publish " .. mqtt_dest[1] .. " payload " .. mqtt_valu[1])
m:publish("/home/".. roomID .."/" .. deviceID .. "/" .. mqtt_dest[1], mqtt_valu[1], 0, 0, function()
table.remove(mqtt_dest, 1)
table.remove(mqtt_valu, 1)
end)
end
end
 
tmr.alarm(2, 1000, 1, function() mqttHandle(0); end)
 
m = mqtt.Client("ESP8266".. deviceID, 180)
m:lwt("/lwt", "ESP8266", 0, 0)
m:on("offline", function(con)
ip = wifi.sta.getip()
print ("Mqtt Reconnecting to " .. broker .. " from " .. ip)
tmr.alarm(1, 10000, 0, function()
m:connect(broker, PORT, 0, function(conn)
print("Mqtt Connected to:" .. broker)
end)
end)
end)
 
function mqttPublish(level)
-- ReadDHT22()
print("MQTT update")
PIN = adc.read(0)
table.insert(mqtt_dest, "luminosity")
table.insert(mqtt_valu, PIN)
 
-- table.insert(mqtt_dest, "temperature")
-- table.insert(mqtt_valu, temp)
 
-- table.insert(mqtt_dest, "humidity")
-- table.insert(mqtt_valu, humi)
 
--local volt = node.readvdd33();
--table.insert(mqtt_dest, "voltage")
--table.insert(mqtt_valu, volt/1000) .. "." .. (volt%1000))
 
mqttHandle(0)
end
 
tmr.alarm(0, 1000, 1, function()
if wifi.sta.status() == 5 and wifi.sta.getip() ~= nil then
tmr.stop(0)
m:connect(broker, PORT, 0, function(conn)
print("Mqtt Connected to:" .. broker)
tmr.alarm(0, seconds*1000, 1, function() mqttPublish(0); end)
end)
end
end)

