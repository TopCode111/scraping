import org.jsoup.*;
import org.jsoup.helper.*;
import org.jsoup.nodes.*;
import org.jsoup.select.*;

import java.io.*; // Only needed if scraping a local File.

public class Scraper {


	public Scraper() {

		Document doc = null;

		try {
			doc = Jsoup.connect("https://guardian.services/product/nightfall-exclusive-rewards/index.html").get();
		} catch (IOException ioe) {
			ioe.printStackTrace();
		}
		Element table = doc.getElementById("all_item_container");
		Elements rows = table.getElementsById("single_item Legendary");
		
		for (Element row : rows) {
            Elements tds = row.getElementsById("text_container");
            for (Element td : tds) {
                Elements spans = row.getElementsByTag("span");
                for (int j = 0; j < spans.size(); j++) {

                    if (j==0) Element name = spans.get(j).text();
                    if (j==1) Element type = spans.get(j).text();
                    
                }
            }
		}
	
	}
	
	public static void main (String args[]) {

		new Scraper();
        
    }
    
	
}


