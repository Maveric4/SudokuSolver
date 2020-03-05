using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using uPLibrary.Networking.M2Mqtt;
using Xamarin.Forms;
using Xamarin.Forms.Xaml;

namespace SudokuSolver
{
    [XamlCompilation(XamlCompilationOptions.Compile)]
    public partial class BrokerSetupPage : ContentPage
    {
        private MqttClient client;
        private string clientId;

        public BrokerSetupPage()
        {
            InitializeComponent();
        }

        private void OnConnectBrokerButtonClicked(object sender, EventArgs e)
        {
            Application.Current.Properties["BrokerIP"] = EntryBrokerIP.Text;
            try
            {
                clientId = Guid.NewGuid().ToString();
                client = new MqttClient(Application.Current.Properties["BrokerIP"] as string);
                client.Connect(clientId);
                Application.Current.Properties["client"] = client;
                Navigation.PushAsync(new MainPage());
            }
            catch (Exception ex)
            {
                //Navigation.PushAsync(new BrokerSetupPage());
                Debug.WriteLine("{0} Exception caught.", ex);
            }
        }
    }
}