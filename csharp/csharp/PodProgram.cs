namespace PodProgram;

class Spravy
{
    string sprava1;
    string sprava2;
    public string Sprava1
    {
        get { return sprava1; } 
        set {  sprava1 = value; }
    }

    public string Sprava2
    {
        get { return sprava2; }
        set { sprava2 = value; }
    }
    public void PosliSpravu(string str)
    {
        Console.WriteLine(str);
    }
}