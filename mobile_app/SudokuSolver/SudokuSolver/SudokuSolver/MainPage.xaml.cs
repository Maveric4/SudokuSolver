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
using Plugin.Media;
using Plugin.Media.Abstractions;
using System.IO;

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
            client.Subscribe(new string[] { "sudoku/#" }, new byte[] { MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE });

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

        private async void OnSendPhotoButtonClicked(object sender, EventArgs e)
        {
            //client.Publish("sudoku/photo", Encoding.ASCII.GetBytes("should be photo"));
            await CrossMedia.Current.Initialize();

            if (!CrossMedia.Current.IsPickPhotoSupported)
            {
                await DisplayAlert("Sorry. ", "Pick photo is not supported!", "OK");
                return;
            }

            var file = await CrossMedia.Current.PickPhotoAsync();

            if (file == null)
                return;

            byte[] imageArray = null;
            if (file != null)
            {
                using (MemoryStream ms = new MemoryStream())
                {
                    var stream = file.GetStream();
                    stream.CopyTo(ms);
                    imageArray = ms.ToArray();
                }
            }
            client.Publish("sudoku/photo", imageArray);
        }


        private async void OnTakePhotoButtonClicked(object sender, EventArgs e)
        {
            await CrossMedia.Current.Initialize();

            if (!CrossMedia.Current.IsCameraAvailable || !CrossMedia.Current.IsTakePhotoSupported)
            {
                await DisplayAlert("No camera", ":( No camera available.", "OK");
                return;
            }

            var file = await CrossMedia.Current.TakePhotoAsync(
                new StoreCameraMediaOptions
                {
                    SaveToAlbum = true,
                });
            if (file == null)
                return;

            PathLabel.Text = file.AlbumPath;

            TakenImage.Source = ImageSource.FromStream(() =>
            {
                var stream = file.GetStream();
                file.Dispose();
                return stream;
            });
        }

        private async void OnPickPhotoButtonClicked(object sender, EventArgs e)
        {
            await CrossMedia.Current.Initialize();

            if (!CrossMedia.Current.IsPickPhotoSupported)
            {
                await DisplayAlert("Sorry. ", "Pick photo is not supported!", "OK");
                return;
            }

            var file = await CrossMedia.Current.PickPhotoAsync();

            if (file == null)
                return;

            PathLabel.Text = "Photo path: " + file.Path;

            PickImage.Source = ImageSource.FromStream(() =>
            {
                var stream = file.GetStream();
                file.Dispose();
                return stream;
            });
        }
    }
}
