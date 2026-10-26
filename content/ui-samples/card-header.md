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
    <layout classNames="card-header">
        <card id="card" width="30em"
              themeNames="cover-media elevated outlined">
            <headerPrefix>
                <avatar image="icons/jmix-icon.png"/>
            </headerPrefix>
            <header>
                <flexLayout flexDirection="COLUMN_REVERSE" classNames="header">
                    <h2 text="Jmix"/>
                    <div text="Modern Dev platform" classNames="subtitle"/>
                </flexLayout>
            </header>
            <headerSuffix>
                <badge text="Fullstack" themeNames="success"/>
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




card-header.css


.card-header .header {
    line-height: var(--aura-line-height-xs);
}

.card-header .subtitle {
    text-transform: uppercase;
    color: var(--vaadin-text-color-secondary);
    font-size: var(--aura-font-size-xs);
}


