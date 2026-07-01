<Path>Components > File Upload Fields > FileStorageUploadField</Path>

The fileStorageUploadField component uploads files to the Jmix FileStorage. It allows users to upload a file and automatically links it to an entity attribute as a FileRef object. The FileRef serves as a reference to the file's location in the file storage. This example allows uploading of files of any type with a size limit of 50 KB. The component features a "drop zone" for drag-and-drop uploads, activated by dragging files over the component's button. Note: In this example, files are uploaded to the temporary storage and immediately removed. See the comments in FileStorageUploadFieldSample.java.

file-storage-upload-field.xml

<view xmlns="http://jmix.io/schema/flowui/view">
<data>
    <instance id="documentDc" class="io.jmix.uisamples.entity.Document">
    </instance>
</data>
<layout>
    <fileStorageUploadField id="fileStorageUploadField" label="Select File"
                            dataContainer="documentDc" property="content"
                            fileNameVisible="false"
                            dropAllowed="true"
                            maxFileSize="51200"
                            fileStoragePutMode="MANUAL"
    />
</layout>
</view>




FileStorageUploadFieldSample.java

package io.jmix.uisamples.view.flowui.components.fileuploadfields.filestorageuploadfield;

import com.vaadin.flow.component.notification.NotificationVariant;
import io.jmix.core.FileRef;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.component.upload.FileStorageUploadField;
import io.jmix.flowui.kit.component.upload.event.FileUploadSucceededEvent;
import io.jmix.flowui.upload.TemporaryStorage;
import io.jmix.flowui.view.*;
import org.springframework.beans.factory.annotation.Autowired;

import java.io.File;
import java.util.UUID;

@ViewController("file-storage-upload-field")
@ViewDescriptor("file-storage-upload-field.xml")
public class FileStorageUploadFieldSample extends StandardView {

    @ViewComponent
    private FileStorageUploadField fileStorageUploadField;

    @Autowired
    private TemporaryStorage temporaryStorage;
    @Autowired
    private Notifications notifications;

    // This handler is needed only when fileStoragePutMode="MANUAL".
    // In AUTO mode the field automatically moves the uploaded file from temporary storage
    // to the FileStorage and sets the returned FileRef to the entity attribute.
    @Subscribe("fileStorageUploadField")
    public void onFileStorageUploadFieldFileUploadSucceeded(
            final FileUploadSucceededEvent<FileStorageUploadField, TemporaryStorage.FileInfo> event) {
        UUID fileId = event.getData().getId();
        File file = temporaryStorage.getFile(fileId);

        if (file != null) {
            FileRef fileRef = new FileRef("tempStorage", file.getAbsolutePath(), file.getName());
            fileStorageUploadField.setValue(fileRef);
            notifications.create("Your file %s has been uploaded successfully.".formatted(event.getFileName()))
                    .withThemeVariant(NotificationVariant.LUMO_PRIMARY)
                    .show();

            // Remove the uploaded file.
            // In a real-world application you would move the file to FileStorage here using
            // the temporaryStorage.putFileIntoStorage() method.
            temporaryStorage.deleteFile(fileId);
        }
    }
}




Document.java

package io.jmix.uisamples.entity;

import io.jmix.core.FileRef;
import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.entity.annotation.JmixId;
import io.jmix.core.metamodel.annotation.JmixEntity;
import io.jmix.core.metamodel.annotation.JmixProperty;

import java.util.UUID;

@JmixEntity
public class Document {

    @JmixGeneratedValue
    @JmixId
    private UUID id;

    @JmixProperty
    private FileRef content;

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    public FileRef getContent() {
        return content;
    }

    public void setContent(FileRef content) {
        this.content = content;
    }
}


