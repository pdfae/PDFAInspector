import java.io.*;
import java.util.*;

public class Test {
	
	public static void main(String[] args)
	{
		try{
			String in1str;
			String in2str;
			BufferedReader in1 = new BufferedReader(new FileReader("files/jsonObj.txt"));
			BufferedReader in2 = new BufferedReader(new FileReader("files/Rules.txt"));
			BufferedWriter out = new BufferedWriter(new FileWriter("files/JS.txt"));
			
			out.write("root = ");
			while((in1str = in1.readLine()) != null)
			{
				out.write(in1str);
			}
			out.write("\n\n");
			while((in2str = in2.readLine()) != null)
			{
				out.write(in2str + "\n");
			}
			
			in1.close();
			in2.close();
			out.close();
		}catch(Exception e){System.err.println("combine two js text files: " + e.getMessage());}
	}
}
