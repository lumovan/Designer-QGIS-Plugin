import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
/*
class TestApp {

    public static void main(String[] args) {

        System.out.println("Dit is een java commando !"); // Display the string.
        int firstArg;
        if (args.length > 0) {
            try {
                firstArg = Integer.parseInt(args[0]);
            } catch (NumberFormatException e) {
                System.err.println("Argument must be an integer!");
                System.out.println("klaar (System exit(1)) !!");
                System.exit(1);
            }
        }

        //Custom button text
        Object[] options = {"Yes, please",
                            "No, thanks",
                            "No eggs, no ham!"};
        int n = JOptionPane.showOptionDialog(frame,
            "Would you like some green eggs to go "
            + "with that ham?",
            "A Silly Question",
            JOptionPane.YES_NO_CANCEL_OPTION,
            JOptionPane.QUESTION_MESSAGE,
            null,
            options,
            options[2]);


        System.out.println("gekozen: " + n);
        System.out.println("klaar (System exit(0)) !!"); // Display the string
        System.exit(0);
    }

}
*/
public final class TestApp {
  
  /** 
   Build and display minimal GUI.
   
   <P>The GUI has a label and an OK button.
   The OK button launches a simple message dialog.
   No menu is included.
  */
  public static void main(String aArgs[]){
    TestApp app = new TestApp();
    app.buildAndDisplayGui(aArgs);
  }
  
  // PRIVATE //

  private void buildAndDisplayGui(String opts[]){
    JFrame frame = new JFrame("Test Frame"); 
    buildContent(frame, opts);
    frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    frame.pack();
    frame.setVisible(true);
  }
  
  private void buildContent(JFrame aFrame, String options[]){
    JPanel panel = new JPanel();
    String opt = "no parameter";
    if (options.length > 0){
        opt = options[0];
    }
    //panel.add(new JLabel("Klik op OK om een dialoog te tonen, kies een van de opties"));
    panel.add(new JLabel("Called with: '"+opt+"' as parameter, click OK to exit"));
    JButton ok = new JButton("OK");
    ok.addActionListener( new ShowDialog(aFrame)  );
    panel.add(ok);
    aFrame.getContentPane().add(panel);
  }

  private static final class ShowDialog implements ActionListener {
    /** Defining the dialog's owner JFrame is highly recommended. */
    ShowDialog(JFrame aFrame){
      fFrame = aFrame;
    }
    public void actionPerformed(ActionEvent aEvent) {

//      JOptionPane.showMessageDialog(fFrame, "This is a dialog");
/*
        //Custom button text                                                     
        Object[] options = {"Optie 0",                                       
                            "Optie 1",                                        
                            "Optie 2"};                                 
        int n = JOptionPane.showOptionDialog(fFrame,                              
            "Optie 0 "                              
            + "Optie 1",                                                  
            "Optie 3",                                                  
            JOptionPane.YES_NO_CANCEL_OPTION,                                    
            JOptionPane.QUESTION_MESSAGE,                                        
            null,                                                                
            options,                                                             
            options[2]);    
        System.out.println("gekozen: " + n);
        //System.out.println("klaar (System exit(0)) !!"); // Display the string
        System.exit(n);
*/

        System.exit(0);

    }
    private JFrame fFrame;
  }
}
