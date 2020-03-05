using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Xamarin.Forms;
using Xamarin.Forms.Xaml;

namespace SudokuSolver
{
    [XamlCompilation(XamlCompilationOptions.Compile)]
    public partial class SolutionPage : ContentPage
    {
        public SolutionPage()
        {
            InitializeComponent();
            if (Application.Current.Properties.ContainsKey("SolvedSudokuImage"))
            {
                SolvedSudokuImage.Source = Application.Current.Properties["SolvedSudokuImage"] as ImageSource;
            }
            else
            {
                TopLabel.Text = "SolvedSudokuImage not found :(";
            }
        }
    }
}