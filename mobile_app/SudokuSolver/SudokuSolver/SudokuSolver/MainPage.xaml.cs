using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Xamarin.Forms;
using uPLibrary.Networking.M2Mqtt;
using uPLibrary.Networking.M2Mqtt.Messages;
using System.Net;

namespace SudokuSolver
{
    // Learn more about making custom code visible in the Xamarin.Forms previewer
    // by visiting https://aka.ms/xamarinforms-previewer
    [DesignTimeVisible(false)]
    public partial class MainPage : ContentPage
    {
        MqttClient client;
        string mqttMSG = string.Empty;
        string topic = string.Empty;
        string MQTT_BROKER_ADDRESS = "192.168.9.201";
        public MainPage()
        {
            InitializeComponent();
            client = new MqttClient(IPAddress.Parse(MQTT_BROKER_ADDRESS));

            // register to message received 
            client.MqttMsgPublishReceived += client_MqttMsgPublishReceived;

            string clientId = Guid.NewGuid().ToString();
            client.Connect(clientId);
            client.Subscribe(new string[] { "sudoku/msg" }, new byte[] { MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE });
        }

        void client_MqttMsgPublishReceived(object sender, MqttMsgPublishEventArgs e)
        {
            mqttMSG = System.Text.Encoding.UTF8.GetString(e.Message);
            topic = e.Topic;
        }

        void OnShowMsgButtonClicked(object sender, EventArgs e)
        {
            LabelTopic.Text = topic;
            LabelMsg.Text = mqttMSG;
        }
    }
}
