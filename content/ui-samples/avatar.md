<Path>Components > Avatar</Path>

A avatar can contain a name, an abbreviation, an icon. By default, the abbreviation is the first characters of the name. The size can be specified using the themeNames attribute: xlarge large small xsmall

avatar.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <details summaryText="Simple avatar" opened="true">
            <hbox padding="false" wrap="true">
                <avatar name="Homer Jay Simpson"/>
                <avatar name="Homer Jay Simpson" abbreviation="HS"/>
                <avatar id="avatarWithImage"/>
            </hbox>
        </details>
        <details summaryText="Theme variants" opened="true">
            <hbox padding="false" wrap="true">
                <avatar abbreviation="XL" themeNames="xlarge"/>
                <avatar abbreviation="L" themeNames="large"/>
                <avatar abbreviation="M"/>
                <avatar abbreviation="S" themeNames="small"/>
                <avatar abbreviation="XS" themeNames="xsmall"/>
            </hbox>
        </details>
    </layout>
</view>




AvatarSample.java

package io.jmix.uisamples.view.flowui.components.avatar;

import com.vaadin.flow.component.avatar.Avatar;
import com.vaadin.flow.server.streams.DownloadHandler;
import io.jmix.core.Resources;
import io.jmix.flowui.view.*;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("avatar")
@ViewDescriptor("avatar.xml")
public class AvatarSample extends StandardView {

    @ViewComponent
    protected Avatar avatarWithImage;

    @Autowired
    protected Resources resources;

    @Subscribe
    protected void onInit(InitEvent event) {
        avatarWithImage.setImageHandler(
                DownloadHandler.forClassResource(getClass(), "/META-INF/resources/icons/homer-simpson.png")
        );
    }
}


