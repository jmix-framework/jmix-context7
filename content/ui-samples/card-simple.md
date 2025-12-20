<Path>Layouts > Card > Simple Card</Path>

The `Card` component is a universal container for displaying content in the form of a card. The component contains
several predefined slots for customization.

The following slots are supported:

* `title` – card title can be set using an attribute or nested element
* `subTitle` – card subtitle can be set using an attribute or nested element
* `headerPrefix` – component before the header, most often it is `avatar` and similar components
* `header` – allows setting custom markup for the header (replaces `title` and `subtitle`)
* `headerSuffix`– component after the header
* `media`– media content for the card (image, avatar, etc.) can be styled using [
  `themeVariant`]({contextPath}/sample/card-theme-variant)
* `content`– markup for the main content of the card
* `footer`– markup for the footer of the card

All slots except `content` and `footer` can contain only one nested component.


card-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <card id="card" width="30em"
              themeNames="cover-media elevated outlined"
              title="msg://card.title" subtitle="msg://card.subtitle">
            <media>
                <image resource="icons/jmix-background.png"/>
            </media>
            <headerPrefix>
                <avatar image="icons/jmix-icon.png"/>
            </headerPrefix>
            <content>
                <p text="msg://card.content.text"/>
            </content>
            <footer>
                <button id="visitSiteButton" text="msg://visitSiteButton.text" icon="EXTERNAL_LINK" themeNames="primary"
                        iconAfterText="true"/>
                <button id="learnMoreButton" text="msg://learnMoreButton.text" icon="QUESTION"
                        iconAfterText="true"/>
            </footer>
        </card>
    </layout>
</view>




CardSimpleSample.java

package io.jmix.uisamples.view.flowui.containers.card.simple;

import com.vaadin.flow.component.ClickEvent;
import com.vaadin.flow.component.UI;
import io.jmix.core.Messages;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.Subscribe;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("card-simple")
@ViewDescriptor("card-simple.xml")
public class CardSimpleSample extends StandardView {

    @Autowired
    private Messages messages;

    @Subscribe("visitSiteButton")
    public void onVisitSiteButtonClick(final ClickEvent<JmixButton> event) {
        UI.getCurrent().getPage().open(messages.getMessage("websiteUrl"));
    }

    @Subscribe("learnMoreButton")
    public void onLearnMoreButtonClick(final ClickEvent<JmixButton> event) {
        UI.getCurrent().getPage().open(messages.getMessage("docUrl"));
    }
}


