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

    [DesignTimeVisible(false)]
    public partial class MainPage : ContentPage
    {
        private MqttClient client;
        string mqttMSG = string.Empty;
        string topic = string.Empty;
        public MainPage()
        {
            InitializeComponent();
            if (Application.Current.Properties.ContainsKey("client"))
            {
                client = Application.Current.Properties["client"] as MqttClient;

                // register to message received 
                client.MqttMsgPublishReceived += client_MqttMsgPublishReceived;

                // subscribe to every sudoku topic
                client.Subscribe(new string[] { "sudoku/#" }, new byte[] { MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE });
            }
        }

        private void client_MqttMsgPublishReceived(object sender, MqttMsgPublishEventArgs e)
        {
            topic = e.Topic;
            if(topic == "sudoku/solution/photo2")
            {
                SolutionImage.Source = ImageSource.FromStream(() => new MemoryStream(e.Message));
                SolutionLabel.IsVisible = true;
                mqttMSG = "Photo with solution";
            }
            else if (topic == "sudoku/solution/photo")
            {
                Application.Current.Properties["SolvedSudokuImage"] = ImageSource.FromStream(() => new MemoryStream(e.Message));
                Device.BeginInvokeOnMainThread(() =>
                {
                    ShowSolutionButton.IsEnabled = true;
                });
            }
            else
            {
                mqttMSG = System.Text.Encoding.UTF8.GetString(e.Message);
            }
        }

        void OnShowMsgButtonClicked(object sender, EventArgs e)
        {
            LabelTopic.Text = topic;
            LabelMsg.Text = mqttMSG;
        }

        void OnShowSolutionButtonClicked(object sender, EventArgs e)
        {
            ShowSolutionButton.IsEnabled = false;
            Navigation.PushAsync(new SolutionPage());
        }

        private async void OnSendPhotoButtonClicked(object sender, EventArgs e)
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
