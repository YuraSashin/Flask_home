import Model.Pet;
import Services.IRepository;
import Services.PetRepository;
import UserInterface.*;

public class main {
    public static void main(String[] args) throws Exception {

        IRepository <Pet> myFarm = new PetRepository();
        UserInterface.PetController controller = new PetController(myFarm);
        new ConsoleMenu (controller).start();
    }

}    
