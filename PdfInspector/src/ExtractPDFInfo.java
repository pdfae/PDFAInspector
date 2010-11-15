import java.io.*;
import java.util.HashMap;
import java.util.List;

import com.itextpdf.text.pdf.PdfDictionary;
import com.itextpdf.text.pdf.PdfName;
import com.itextpdf.text.pdf.PdfReader;
import com.itextpdf.text.pdf.SimpleBookmark;
import com.itextpdf.text.pdf.parser.TaggedPdfReaderTool;

public class ExtractPDFInfo {

    public static void main(String[] args) throws IOException {
    	
        try {
        	String filename = "tables-example2";
        	String pathname = "C:/Users/Karen/Documents/Homework/PDF_Tests/pdfainspector/testcases/" +
        			filename + ".pdf";
        	PdfExtractor extractor = new PdfExtractor(pathname);
        	
        	String tagFilename = "C:/Users/Karen/Documents/Homework/PDF_Tests/pdfainspector/testcases/itext-" +
				filename + ".xml";
            File tags = extractor.extractTags(tagFilename);
            
            String formFilename = "C:/Users/Karen/Documents/Homework/PDF_Tests/pdfainspector/testcases/form-" +
				filename + ".xml";
            File forms = extractor.extractForm(formFilename);
            
            String bookFilename ="C:/Users/Karen/Documents/Homework/PDF_Tests/pdfainspector/testcases/bookmarks-" +
				filename + ".xml";
            File bookmarks = extractor.extractBookmarks(bookFilename);
            
            PdfInfo info = new PdfInfo(tags, forms, bookmarks);
            info.exportAsXML("C:/Users/Karen/Documents/Homework/PDF_Tests/pdfainspector/testcases/final-" +
				filename + ".xml");
        } catch (Exception e) {
        }
    }
    

}
