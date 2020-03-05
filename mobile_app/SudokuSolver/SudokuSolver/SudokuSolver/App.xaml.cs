using System;
using System.Net;
using Xamarin.Forms;
using Xamarin.Forms.Xaml;
using uPLibrary.Networking.M2Mqtt;
using uPLibrary.Networking.M2Mqtt.Messages;

namespace SudokuSolver
{
    public partial class App : Application
    {
        private MqttClient client;
        private string clientId;

        public App()
        {
            InitializeComponent();
            Application.Current.Properties["BrokerIP"] = "192.168.9.201";
            MainPage = new NavigationPage(new MainPage());
        }

        protected override void OnStart()
        {
            // Handle when your app starts
            clientId = Guid.NewGuid().ToString();
            client = new MqttClient(Application.Current.Properties["BrokerIP"] as string);
            try
            {
                client.Connect(clientId);
                Application.Current.Properties["client"] = client;
            }
            catch(Exception e)
            {
                MainPage = new NavigationPage(new BrokerSetupPage());
            }
        }

        protected override void OnSleep()
        {
            // Handle when your app sleeps

        }

        protected override void OnResume()
        {
            // Handle when your app resumes
            
        }
    }
}
