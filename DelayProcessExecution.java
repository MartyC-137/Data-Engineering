//Delay process execution in Boomi
//By: Martin Palkovic
//Date: 2022-02-23

import java.util.Properties;
import java.io.InputStream;

// Specify the length of time to wait in seconds.
int waitFor = 2;

Thread.sleep(waitFor * 1000);

// Leave the rest of the script as-is to pass the Documents to the next step.
for ( int i = 0; i < dataContext.getDataCount(); i++ ) {
    InputStream is = dataContext.getStream(i);
    Properties props = dataContext.getProperties(i);

    dataContext.storeStream(is, props);
}
