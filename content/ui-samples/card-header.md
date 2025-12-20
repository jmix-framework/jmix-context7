<Path>Layouts > Card > Card with header</Path>

The `header` element in the `Card` component allows you to specify custom markup for the header. It replaces the values
of `title` and `subtitle`.

The following list shows the display priorities of header settings:

1. `header`
2. `title` and `subtitle` nested elements in `card`
3. `title` and `subtitle` attributes of `card`

According to this list, when multiple header settings are specified at the same time, the one with the highest priority
will be displayed.


card-header.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <card id="card" width="30em"
              themeNames="cover-media elevated outlined">
            <headerPrefix>
                <avatar image="icons/jmix-icon.png"/>
            </headerPrefix>
            <header>
                <div classNames="flex flex-col-reverse leading-xs">
                    <h2 text="Jmix"/>
                    <div text="Modern Dev platform" classNames="uppercase text-xs text-secondary"/>
                </div>
            </header>
            <headerSuffix>
                <span text="Fullstack" themeNames="badge success"/>
            </headerSuffix>
        </card>
    </layout>
</view>




CardHeaderSample.java

package io.jmix.uisamples.view.flowui.containers.card.header;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("card-header")
@ViewDescriptor("card-header.xml")
public class CardHeaderSample extends StandardView {
}


