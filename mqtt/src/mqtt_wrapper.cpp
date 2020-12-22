#include <inc/mqtt_wrapper.h>

#include <iostream>
#include <cstdlib>
#include <string>
#include <thread>
#include <atomic>
#include <chrono>
#include <cstring>
#include "mqtt/async_client.h"

using namespace std;

const std::string DFLT_SERVER_ADDRESS	{ "broker.hivemq.com:1883" };
const std::string DFLT_CLIENT_ID		{ "async_publish" };

// const string TOPIC { "hello" };
// const string TOPIC { "hello2" };


// const char* PAYLOAD1 = "RASPBERRY";
// const char* PAYLOAD2 = "SIE WITA";
// const char* PAYLOAD3 = "KOZAK?";
// const char* PAYLOAD4 = "Wiadomo";

const char* LWT_PAYLOAD = "Last will and testament.";

const int  QOS = 1;

const auto TIMEOUT = std::chrono::seconds(10);

class callback : public virtual mqtt::callback
{
public:
	void connection_lost(const string& cause) override {
		cout << "\nConnection lost" << endl;
		if (!cause.empty())
			cout << "\tcause: " << cause << endl;
	}

	void delivery_complete(mqtt::delivery_token_ptr tok) override {
		cout << "\tDelivery complete for token: "
			<< (tok ? tok->get_message_id() : -1) << endl;
	}
};

class action_listener : public virtual mqtt::iaction_listener
{
protected:
	void on_failure(const mqtt::token& tok) override {
		cout << "\tListener failure for token: "
			<< tok.get_message_id() << endl;
	}

	void on_success(const mqtt::token& tok) override {
		cout << "\tListener success for token: "
			<< tok.get_message_id() << endl;
	}
};

class delivery_action_listener : public action_listener
{
	atomic<bool> done_;

	void on_failure(const mqtt::token& tok) override {
		action_listener::on_failure(tok);
		done_ = true;
	}

	void on_success(const mqtt::token& tok) override {
		action_listener::on_success(tok);
		done_ = true;
	}

public:
	delivery_action_listener() : done_(false) {}
	bool is_done() const { return done_; }
};

int MqttWrapper::Publisher(const char* PAYLOAD4, const string TOPIC)
{
	string	address  = DFLT_SERVER_ADDRESS,
			clientID = DFLT_CLIENT_ID;

	cout << "Initializing for server '" << address << "'..." << endl;
	mqtt::async_client client(address, clientID);

	callback cb;
	client.set_callback(cb);

	mqtt::connect_options conopts;
	mqtt::message willmsg(TOPIC, LWT_PAYLOAD, 1, true);
	mqtt::will_options will(willmsg);
	conopts.set_will(will);

	cout << "  ...OK" << endl;

	try {
		cout << "\nConnecting..." << endl;
		mqtt::token_ptr conntok = client.connect(conopts);
		cout << "Waiting for the connection..." << endl;
		conntok->wait();
		cout << "  ...OK" << endl;

		mqtt::message_ptr pubmsg; // to delete supressing compile error!!!
		cout << "\nSending final message..." << endl;
		delivery_action_listener deliveryListener;
		pubmsg = mqtt::make_message(TOPIC, PAYLOAD4);
		client.publish(pubmsg, nullptr, deliveryListener);

		while (!deliveryListener.is_done()) {
			this_thread::sleep_for(std::chrono::milliseconds(100));
		}
		cout << "OK" << endl;


		// Disconnect
		cout << "\nDisconnecting..." << endl;
		conntok = client.disconnect();
		conntok->wait();
		cout << "  ...OK" << endl;
	}
	catch (const mqtt::exception& exc) {
		cerr << exc.what() << endl;
		return 1;
	}

 	return 0;
}
