<Path>Components > Badge > Simple Badge</Path>

badge is a special theme variant available to all HTML container components.

badge-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout classNames="horizontal-layout">
        <span text="Pending" themeNames="badge normal"/>
        <span text="Confirmed" themeNames="badge success"/>
        <span text="Warning" themeNames="badge warning"/>
        <span text="Denied" themeNames="badge error"/>
        <span text="On hold" themeNames="badge contrast"/>
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


