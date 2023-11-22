using PodProgram;

string text1 = new Spravy().Sprava1;
string text2 = new Spravy().Sprava2;
Spravy spravy = new Spravy();
text1 = "Chces spustit static alebo non-static metodu? [static/non-static] ";
text2 = "Co chces aby ti kod vypisal?";

DruhaKlasa druha = new DruhaKlasa();

spravy.PosliSpravu(text1);
string vstup = Console.ReadLine();
spravy.PosliSpravu(text2);
string vypis = Console.ReadLine();
druha.Vypis = vypis;


if (vstup == "static")
{
    DruhaKlasa.Vypis2(druha.Vypis);
}
else if (vstup == "non-static")
{
    druha.Vypis3(druha.Vypis);
}

class DruhaKlasa
{
    public string vypis;

    public string Vypis
    {
        get { return vypis; }
        set { vypis = value; }
    }
    public static void Vypis2(string vypis)
    {
        Console.WriteLine("----------------------------------");
        Console.WriteLine(vypis);
    }
    public void Vypis3(string vypis)
    {
        Console.WriteLine("----------------------------------");
        Console.WriteLine(vypis);
        
    }
}
