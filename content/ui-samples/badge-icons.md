<Path>Components > Badge > Badge with icons</Path>

All content of the badged component also becomes badged. This sample shows an example of an icon with a badge.

badge-icons.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <details summaryText="Simple icon" opened="true">
            <vbox padding="false">
                <hbox wrap="true">
                    <span themeNames="badge normal">
                        <icon icon="CLOCK" classNames="badged-icon"/>
                        <span text="Pending"/>
                    </span>
                    <span themeNames="badge success">
                        <icon icon="CHECK" classNames="badged-icon"/>
                        <span text="Confirmed"/>
                    </span>
                    <span themeNames="badge warning">
                        <icon icon="WARNING" classNames="badged-icon"/>
                        <span text="Warning"/>
                    </span>
                    <span themeNames="badge error">
                        <icon icon="EXCLAMATION_CIRCLE_O" classNames="badged-icon"/>
                        <span text="Denied"/>
                    </span>
                    <span themeNames="badge contrast">
                        <icon icon="HAND" classNames="badged-icon"/>
                        <span text="On hold"/>
                    </span>
                </hbox>
                <hbox wrap="true">
                    <span themeNames="badge normal">
                        <span text="Pending"/>
                        <icon icon="CLOCK" classNames="badged-icon"/>
                    </span>
                    <span themeNames="badge success">
                        <span text="Confirmed"/>
                        <icon icon="CHECK" classNames="badged-icon"/>
                    </span>
                    <span themeNames="badge warning">
                        <span text="Warning"/>
                        <icon icon="WARNING" classNames="badged-icon"/>
                    </span>
                    <span themeNames="badge error">
                        <span text="Denied"/>
                        <icon icon="EXCLAMATION_CIRCLE_O" classNames="badged-icon"/>
                    </span>
                    <span themeNames="badge contrast">
                        <span text="On hold"/>
                        <icon icon="HAND" classNames="badged-icon"/>
                    </span>
                </hbox>
            </vbox>
        </details>
        <details summaryText="Icon-Only" opened="true">
            <hbox wrap="true">
                <icon id="checkIcon" icon="CHECK" classNames="badged-icon"/>
                <icon id="closeIcon" icon="CLOSE_SMALL" classNames="badged-icon"/>
            </hbox>
        </details>
    </layout>
</view>




BadgeIconsSample.java

package io.jmix.uisamples.view.flowui.components.badge.icons;

import com.vaadin.flow.component.icon.Icon;
import io.jmix.flowui.view.*;

@ViewController("badge-icons")
@ViewDescriptor("badge-icons.xml")
public class BadgeIconsSample extends StandardView {

    @ViewComponent
    protected Icon checkIcon;
    @ViewComponent
    protected Icon closeIcon;

    @Subscribe
    protected void onInit(InitEvent event) {
        checkIcon.getElement().getThemeList().add("badge success");
        checkIcon.getStyle().set("padding", "4px");

        closeIcon.getElement().getThemeList().add("badge error");
        closeIcon.getStyle().set("padding", "4px");
    }
}




badge-icons.css


.badged-icon {
    box-sizing: content-box;
}

.badged-icon[theme~="badge"] {
    min-width: 1em;
    gap: 0;
}


