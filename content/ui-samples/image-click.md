<Path>Components > Image > Image click listener</Path>

Image component can handle click event.

image-click.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout classNames="items-center">
        <h4 text="Image to click"/>
        <image id="image" resource="icons/jmix-icon.png" height="15em" width="15em"/>
    </layout>
</view>




ImageClickSample.java

package io.jmix.uisamples.view.flowui.components.image.click;

import com.vaadin.flow.component.ClickEvent;
import com.vaadin.flow.component.Html;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.component.image.JmixImage;
import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.Subscribe;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("image-click")
@ViewDescriptor("image-click.xml")
public class ImageClickSample extends StandardView {

    @Autowired
    protected Notifications notifications;

    @Subscribe("image")
    protected void onImageClick(ClickEvent<JmixImage<?>> event) {
        Html html = new Html(getNotificationContent(event));
        notifications.show(html);
    }

    protected String getNotificationContent(ClickEvent<JmixImage<?>> event) {
        return String.format("<div><strong>Click info:</strong>"
                        + "<br><strong>Client X:</strong> %s"
                        + "<br><strong>Client Y:</strong> %s"
                        + "<br><strong>Is Ctrl click:</strong> %s"
                        + "<br><strong>Is Alt click:</strong> %s<br>"
                        + "<strong>Is Shift click:</strong> %s</div>",
                event.getClientX(), event.getClientY(),
                event.isCtrlKey(), event.isAltKey(), event.isShiftKey());
    }
}


