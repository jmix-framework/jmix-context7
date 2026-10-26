<Path>Components > Image > Data-aware Image</Path>

The dataContainer and property attributes are used to connect the Image to an entity attribute. The dataContainer contains an entity instance; property specifies an attribute to edit.

image-dataaware.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <data>
        <instance id="pictureDc"
                  class="io.jmix.uisamples.entity.Picture"
                  fetchPlan="_local"/>
    </data>
    <layout>
        <fileUploadField label="Load new image" dataContainer="pictureDc" property="content"
                         clearButtonVisible="true" fileNameVisible="true" acceptedFileTypes=".png"/>
        <image height="10em" width="10em"
               alternateText="No picture loaded"
               dataContainer="pictureDc" property="content"/>
    </layout>
</view>




ImageDataawareSample.java

package io.jmix.uisamples.view.flowui.components.image.dataaware;

import io.jmix.core.Metadata;
import io.jmix.core.Resources;
import io.jmix.flowui.model.InstanceContainer;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Picture;
import org.springframework.beans.factory.annotation.Autowired;

import java.io.IOException;
import java.io.UncheckedIOException;

@ViewController("image-dataaware")
@ViewDescriptor("image-dataaware.xml")
public class ImageDataawareSample extends StandardView {

    private static final String SRC_PATH = "META-INF/resources/icons/jmix-icon.png";

    @ViewComponent
    private InstanceContainer<Picture> pictureDc;

    @Autowired
    private Metadata metadata;
    @Autowired
    private Resources resources;

    @Subscribe
    public void onInit(InitEvent event) {
        Picture picture = metadata.create(Picture.class);

        try {
            picture.setContent(resources.getResource(SRC_PATH).getContentAsByteArray());
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }

        pictureDc.setItem(picture);
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


