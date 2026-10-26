<Path>Components > Badge > Simple Badge</Path>

`Badge` is a component for displaying a small piece of information – a status, a count or a label.

Theme variants set the color: `success`, `warning` and `error`. Without a variant the badge uses the theme accent color.



badge-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout classNames="horizontal-layout">
        <badge id="pendingBadge" text="Pending"/>
        <badge id="confirmedBadge" text="Confirmed" themeNames="success"/>
        <badge id="warningBadge" text="Warning" themeNames="warning"/>
        <badge id="deniedBadge" text="Denied" themeNames="error"/>
    </layout>
</view>




BadgeSimpleSample.java

package io.jmix.uisamples.view.flowui.components.badge.simple;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("badge-simple")
@ViewDescriptor("badge-simple.xml")
public class BadgeSimpleSample extends StandardView {
}


