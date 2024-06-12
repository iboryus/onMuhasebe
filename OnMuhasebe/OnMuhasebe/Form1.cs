using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace OnMuhasebe
{
    public partial class Form1 : Form
    {
        private const string dKullaniciAdi = "iboryus";
        private const string dSifre = "sifre";
        public Form1()
        {
            InitializeComponent();
        }

        private void giris_Click(object sender, EventArgs e)
        {
            string username = kullaniciAdi.Text;
            string password = sifre.Text;

            if (username == dKullaniciAdi && password == dSifre)
            {
                anaGiris anagiris = new anaGiris();
                anagiris.Show();
                this.Hide();
            }
            else
            {
                MessageBox.Show("Kullanıcı Adı Şifre Hatalı", "Hata", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }
}
