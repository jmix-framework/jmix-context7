<Path>Layouts > Split > Simple Split</Path>

split is a layout that creates two content areas divided by a draggable splitter. The default split orientation is vertical, but it can be changed to horizontal by orientation attribute. The starting position of the splitter can be specified using the splitterPosition attribute.

split-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <split width="100%" themeNames="splitter-spacing" splitterPosition="45">
            <textArea label="TextArea1" width="100%" height="100%"/>
            <split orientation="VERTICAL">
                <textArea label="TextArea2" width="100%" height="100%"/>
                <textArea label="TextArea3" width="100%" height="100%"/>
            </split>
        </split>
    </layout>
</view>




SplitSimpleSample.java

package io.jmix.uisamples.view.flowui.containers.split.simple;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("split-simple")
@ViewDescriptor("split-simple.xml")
public class SplitSimpleSample extends StandardView {
}


