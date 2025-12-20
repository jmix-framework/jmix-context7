<Path>Components > File Upload Fields > Upload</Path>

The upload component allows users to upload one or multiple files. It shows the upload progress and the status of each file. Files can be uploaded by clicking on the Upload files button or by dragging them onto the component zone. This example allows uploading up to 3 files with a maximum size of 10 KB each. The name of the uploaded file appears next to its corresponding uploaded file. This example uses a MultiFileMemoryBuffer to handle multiple files and write file data into a set of in-memory buffers. For uploading and saving large files, it is recommended to use the FileStorageUploadField.

upload.xml

<view xmlns="http://jmix.io/schema/flowui/view">
<layout>
    <upload id="upload"
                     dropAllowed="true"
                     maxFileSize="10000"
                     receiverType="MULTI_FILE_MEMORY_BUFFER"
                     maxFiles="3"
    />
</layout>
</view>




UploadSample.java

package io.jmix.uisamples.view.flowui.components.fileuploadfields.upload;

import com.vaadin.flow.component.Html;
import com.vaadin.flow.component.notification.NotificationVariant;
import com.vaadin.flow.component.upload.FileRejectedEvent;
import com.vaadin.flow.component.upload.SucceededEvent;
import com.vaadin.flow.component.upload.receivers.MultiFileMemoryBuffer;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.Subscribe;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;
import org.apache.commons.io.IOUtils;
import org.springframework.beans.factory.annotation.Autowired;

import java.io.IOException;
import java.io.InputStream;

@ViewController("upload")
@ViewDescriptor("upload.xml")
public class UploadSample extends StandardView {

    @Autowired
    private Notifications notifications;

    @Subscribe("upload")
    public void onUploadSucceeded(final SucceededEvent event) {
        StringBuilder sb = new StringBuilder();
        sb.append("<div>Uploaded file: ").append(event.getFileName());
        if (event.getUpload().getReceiver() instanceof MultiFileMemoryBuffer buffer) {
            sb.append("<p>Buffer content:");
            for (String fileName : buffer.getFiles()) {
                try (InputStream inputStream = buffer.getInputStream(fileName)) {
                    byte[] bytes = IOUtils.toByteArray(inputStream);
                    sb.append("<br>File: ").append(fileName).append(", size: ").append(bytes.length);
                } catch (IOException e) {
                    throw new RuntimeException("Error reading file", e);
                }
            }
            sb.append("</p>");
        }
        sb.append("</div>");

        notifications.create(new Html(sb.toString()))
                .withThemeVariant(NotificationVariant.LUMO_PRIMARY)
                .withDuration(5000)
                .show();
    }

    @Subscribe("upload")
    public void onUploadFileRejected(final FileRejectedEvent event) {
        notifications.create(event.getErrorMessage())
                .withThemeVariant(NotificationVariant.LUMO_WARNING)
                .withDuration(5000)
                .show();
    }
}


