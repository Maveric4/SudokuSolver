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

        public App()
        {
            InitializeComponent();
            MainPage = new NavigationPage(new MainPage());
        }

        protected override void OnStart()
        {
            // Handle when your app starts
            //string clientId = Guid.NewGuid().ToString();
            //MqttClient client = new MqttClient(Application.Current.Properties["BrokerIP"] as string);
            //try
            //{
            //    client.Connect(clientId);
            //    MainPage = new NavigationPage(new MainPage());
            //}
            //catch(Exception e)
            //{
            //    MainPage = new NavigationPage(new BrokerSetupPage());
            //}
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
