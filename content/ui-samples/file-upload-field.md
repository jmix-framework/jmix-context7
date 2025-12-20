<Path>Components > File Upload Fields > FileUploadField</Path>

The fileUploadField component provides a way to upload files. It enables users to select and upload a file, automatically saving the file content as a byte array to a specified entity attribute. This example allows uploading of image files (PNG, JPEG) with a maximum size of 50 KB. The name of the uploaded file appears next to the upload button and also functions as a download link for quick access. The component features a "drop zone" for drag-and-drop uploads by dragging files over the component's button. For uploading and saving large files it is recommended to use the FileStorageUploadField.

file-upload-field.xml

<view xmlns="http://jmix.io/schema/flowui/view">
<data>
    <instance id="pictureDc" class="io.jmix.uisamples.entity.Picture">
    </instance>
</data>
<layout>
    <fileUploadField id="fileUploadField" label="Select File"
                     dataContainer="pictureDc" property="content"
                     clearButtonVisible="true"
                     fileNameVisible="true"
                     dropAllowed="true"
                     maxFileSize="51200"
                     acceptedFileTypes="image/png,image/jpeg"
    />
</layout>
</view>




FileUploadFieldSample.java

package io.jmix.uisamples.view.flowui.components.fileuploadfields.fileuploadfield;

import com.vaadin.flow.component.notification.NotificationVariant;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.component.upload.FileStorageUploadField;
import io.jmix.flowui.kit.component.upload.event.FileUploadSucceededEvent;
import io.jmix.flowui.view.*;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("file-upload-field")
@ViewDescriptor("file-upload-field.xml")
public class FileUploadFieldSample extends StandardView {

    @Autowired
    private Notifications notifications;

    @Subscribe("fileUploadField")
    public void onFileUploadFieldFileUploadSucceeded(final FileUploadSucceededEvent<FileStorageUploadField> event) {
        notifications.create("Your file %s has been uploaded successfully.".formatted(event.getFileName()))
                .withThemeVariant(NotificationVariant.LUMO_PRIMARY)
                .show();
    }
}




Picture.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.entity.annotation.JmixId;
import io.jmix.core.metamodel.annotation.JmixEntity;
import io.jmix.core.metamodel.annotation.JmixProperty;

import java.util.UUID;

@JmixEntity
public class Picture {

    @JmixGeneratedValue
    @JmixId
    private UUID id;

    @JmixProperty
    private byte[] content;

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    public byte[] getContent() {
        return content;
    }

    public void setContent(byte[] content) {
        this.content = content;
    }
}


