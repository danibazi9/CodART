package a.aa;
import static a.aa.A;
import vddf.dfdf.A;

class A
{
    class B {
    }

    public int f, c, a; /* printF , printF, */
    public int g; /* printF, printG */
    public string h; /* printH */

    // Method 1
    void printF(int i)
    {
        this.f = i * this.f;
    }

    // Method 2
    void printF(float i){
        this.f = (int) (i * this.f);
        this.g = (int) (i * this.g);
    }

    // Method 3
    void printG(){
        print(this.g);
    }

    // Method 4
    void printH(){
        print(this.h);
    }
}