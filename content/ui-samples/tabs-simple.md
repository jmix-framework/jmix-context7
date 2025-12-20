<Path>Components > Tabs > Simple Tabs</Path>

tabs creates a set of tabs. Unlike tabSheet, it cannot contain tabs content.

tabs-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <tabs width="100%">
            <tab id="issueTab" label="Issues"/>
            <tab id="featureTab" label="Features"/>
            <tab id="bugTab" label="Bugs"/>
        </tabs>
    </layout>
</view>




TabsSimpleSample.java

package io.jmix.uisamples.view.flowui.components.tabs.simple;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("tabs-simple")
@ViewDescriptor("tabs-simple.xml")
public class TabsSimpleSample extends StandardView {
}


