const mqtt = require("mqtt");
const client = mqtt.connect("mqtt://ubidots-balena:1883", {clientId: "main"});

client.on("connect", function (connack) {
  console.log(`[INFO] Connected with result code ${connack.returnCode}`);

  // Subscribe to variable last value
  client.subscribe("humidity/lv");

  // Subscribe to variable last dot
  client.subscribe("temperature");
});

client.on("message", function (topic, message, packet) {
  console.log(
    `[INFO] Receive data from variable\n${topic}: ${message.toString()}`
  );
});

function main() {
  var timestamp = Date.now();

  // Send data to device
  var topic = "/";
  var payload = JSON.stringify({
    humidity: {
      value: (Math.random() * 2 + 50).toFixed(0),
      timestamp: timestamp,
    },
    pressure: {
      value: (Math.random() * 10 + 95).toFixed(1),
      timestamp: timestamp,
    },
  });
  console.log(`[INFO] Send data to device\n${topic}: ${payload}`);
  client.publish(topic, payload, { qos: 0, retain: false });

  // Send data to variable
  var topic = "temperature";
  var payload = JSON.stringify({
    value: (Math.random() * 5 + 25).toFixed(1),
    timestamp: timestamp,
  });
  console.log(`[INFO] Send data to device\n${topic}: ${payload}`);
  client.publish(topic, payload, { qos: 0, retain: false });
}

main();
setInterval(main, 10 * 1000);
