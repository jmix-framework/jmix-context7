<Path>Components > Badge > Badge with icons</Path>

A badge can show an icon next to its text. You can set it using the `icon` attribute or a nested `<icon>` element. The icon is always rendered before the text.

The `icon-only` variant hides the text visually but keeps it available to screen readers, so an icon badge still announces its meaning.


badge-icons.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <details summaryText="Icon and text" opened="true">
            <hbox wrap="true">
                <badge id="pendingBadge" text="Pending" icon="CLOCK"/>
                <badge id="confirmedBadge" text="Confirmed" icon="CHECK" themeNames="success"/>
                <badge id="warningBadge" text="Warning" icon="WARNING" themeNames="warning"/>
                <badge id="deniedBadge" text="Denied" themeNames="error">
                    <icon>
                        <icon icon="EXCLAMATION_CIRCLE"/>
                    </icon>
                </badge>
            </hbox>
        </details>
        <details summaryText="Icon only" opened="true">
            <hbox wrap="true">
                <badge id="confirmedIconBadge" text="Confirmed" icon="CHECK" themeNames="success icon-only"/>
                <badge id="deniedIconBadge" text="Denied" icon="CLOSE" themeNames="error icon-only"/>
            </hbox>
        </details>
    </layout>
</view>




BadgeIconsSample.java

package io.jmix.uisamples.view.flowui.components.badge.icons;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("badge-icons")
@ViewDescriptor("badge-icons.xml")
public class BadgeIconsSample extends StandardView {
}


