public class Sth {
    public static void main(String[] args) {
        try {
            int[] numbers = new int[]{1, 2, 3};
            int index = 4;
            int i;
if (index < numbers.length) {
	 System
	                    .out
                    .println(numbers[index]); }
 else {
            System.out.println("IndexOutOfBoundsException Caught...");
            String index = "0";
        }
 int j; //IndexOutOfBoundsException
        }
        catch (ArrayStoreException exception){
            //sth ...
        }
        finally{
            //sth ...
        }
    }
}