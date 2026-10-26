<Path>Components > Image > Image with resources</Path>

The image component can display images from different resources Static - an image can be served statically by the application. URL - an image can be loaded from an arbitrary URL. ProgrammaticResource - an image can be provided by an DownloadHandler.

image-resources.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout justifyContent="BETWEEN" classNames="horizontal-layout">
        <vbox padding="false" width="AUTO" alignItems="CENTER">
            <h4 text="Static resource"/>
            <image resource="icons/image-sample.svg"
                   height="15em" width="15em"/>
        </vbox>
        <vbox padding="false" width="AUTO" alignItems="CENTER">
            <h4 text="URL resource"/>
            <image resource="https://demo.jmix.io/ui-samples/icons/image-sample.svg"
                   height="15em" width="15em"/>
        </vbox>
        <vbox padding="false" width="AUTO" alignItems="CENTER">
            <h4 text="Programmatic resource"/>
            <image id="imageProgrammaticResource"
                   height="15em" width="15em"/>
        </vbox>
    </layout>
</view>




ImageResourcesSample.java

package io.jmix.uisamples.view.flowui.components.image.resources;

import com.vaadin.flow.server.streams.DownloadHandler;
import io.jmix.flowui.component.image.JmixImage;
import io.jmix.flowui.view.*;

@ViewController("image-resources")
@ViewDescriptor("image-resources.xml")
public class ImageResourcesSample extends StandardView {

    protected static final String SRC_PATH = "/META-INF/resources/icons/image-sample.svg";

    @ViewComponent
    protected JmixImage<?> imageProgrammaticResource;

    @Subscribe
    protected void onInit(InitEvent event) {
        imageProgrammaticResource.setSrc(DownloadHandler.forClassResource(getClass(), SRC_PATH));
    }
}


