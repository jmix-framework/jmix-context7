<Path>Components > TextArea > Resizable TextArea</Path>

To enable resizing for TextArea, use CSS styles. Available variants: both vertical horizontal none

text-area-resizable.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout classNames="horizontal-layout">
        <textArea id="textArea" label="Standard TextArea"/>
        <textArea id="resizableBothTextArea" label="Resizeable TextArea"
                  classNames="resizable-both"
                  themeNames="helper-above-field"
                  helperText="Both direction"/>
        <textArea id="resizableVerticalTextArea" label="Resizeable TextArea"
                  classNames="resizable-vertical"
                  themeNames="helper-above-field"
                  helperText="Vertical direction"/>
        <textArea id="resizableHorizontalTextArea" label="Resizeable TextArea"
                  classNames="resizable-horizontal"
                  themeNames="helper-above-field"
                  helperText="Horizontal direction"/>
    </layout>
</view>




TextAreaResizableSample.java

package io.jmix.uisamples.view.flowui.components.textarea.resizable;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("text-area-resizable")
@ViewDescriptor("text-area-resizable.xml")
public class TextAreaResizableSample extends StandardView {
}




text-area-resizable.css


.resizable-both {
    resize: both;
    overflow: auto;
    padding-bottom: unset;
}

.resizable-vertical {
    resize: vertical;
    overflow: auto;
    padding-bottom: unset;
}

.resizable-horizontal {
    resize: horizontal;
    overflow: auto;
    padding-bottom: unset;
}


