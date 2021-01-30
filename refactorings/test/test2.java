public class Main {
    public static int max(int num1, int num2){
        int index = 0;
        return index;
    }
    public static void main(String[] args) {
        try {
            int[] numbers = new int[]{1, 2, 3};
            int index = 4;
            System.out.println(numbers[index]); //IndexOutOfBoundsException

            Object x[] = new String[3];
            x[0] = 0; //ArrayStoreException

        }
        catch (IndexOutOfBoundsException exception){
            System.out.println("IndexOutOfBoundsException Caught...");
            String index = "0";
        }
        catch (ArrayStoreException exception){
            System.out.println("ArrayStoreException  Caught...");
            char gender = 'm';
        }
        finally {
            System.out.println("Finally...");
        }
    }
}