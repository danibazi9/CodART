public class Main {
    public static void main(String[] args) {
        try {
            int[] numbers = new int[]{1, 2, 3};
            int index = 4;
            System.out.println(numbers[index]); //IndexOutOfBoundsException
        }
        catch (IndexOutOfBoundsException exception){
            System.out.println("IndexOutOfBoundsException Caught...");
            String index = "0";
        }
    }
}