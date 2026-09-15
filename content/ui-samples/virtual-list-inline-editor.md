<Path>Components > VirtualList > VirtualList inline editor</Path>

An example of how to build an inline editor on an entity using VirtualList. Here are the steps you need to take: In the view, declare VirtualList; Generate a Renderer for the created VirtualList; In the Renderer, begin by generating cards of Vertical Layout, each containing the following elements: Avatar - an optional element, placed first in the Vertical Layout (card); Info Layout - any combination of elements that can display information about the current item; Button Layout - a layout containing control buttons for working with the current element; Create a DetailView to edit the selected entity or create a new one; Attach actions to all buttons to control CRUD operations; Your inline editor with VirtualList is ready.

virtual-list-inline-editor.xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<view xmlns="http://jmix.io/schema/flowui/view"
      title="msg://virtualListInlineEditor.title">
    <data>
        <collection id="foodDc" class="io.jmix.uisamples.entity.Food">
            <loader id="foodDl"/>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout>
        <hbox width="100%" padding="false" alignItems="CENTER">
            <h2 id="menusItemsTabTitle" text="msg://foodListTitle"/>
            <button id="addBtn"
                    classNames="virtual-list-inline-editor-add-button"
                    themeNames="primary"
                    icon="PLUS"
                    text="msg:///actions.Add"/>
        </hbox>
        <html id="foodDescription" content="msg://foodListDescription"/>
        <virtualList id="foodList" itemsContainer="foodDc" width="100%"/>
    </layout>
</view>




VirtualListInlineEditorSample.java

package io.jmix.uisamples.view.flowui.components.virtuallist.inlineeditor;


import com.vaadin.flow.component.ClickEvent;
import com.vaadin.flow.component.Html;
import com.vaadin.flow.component.Text;
import com.vaadin.flow.component.avatar.Avatar;
import com.vaadin.flow.component.avatar.AvatarVariant;
import com.vaadin.flow.component.button.Button;
import com.vaadin.flow.component.button.ButtonVariant;
import com.vaadin.flow.component.icon.Icon;
import com.vaadin.flow.component.icon.VaadinIcon;
import com.vaadin.flow.component.orderedlayout.FlexComponent;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.data.renderer.ComponentRenderer;
import com.vaadin.flow.data.renderer.Renderer;
import com.vaadin.flow.server.streams.DownloadHandler;
import com.vaadin.flow.server.streams.DownloadResponse;
import com.vaadin.flow.server.streams.InputStreamDownloadHandler;
import io.jmix.core.LoadContext;
import io.jmix.core.Messages;
import io.jmix.flowui.DialogWindows;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.model.CollectionContainer;
import io.jmix.flowui.model.DataContext;
import io.jmix.flowui.theme.StyleUtility;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.bean.FoodPlaceholderDataGenerator;
import io.jmix.uisamples.entity.Food;
import io.jmix.uisamples.view.entity.food.FoodDetailView;
import org.springframework.beans.factory.annotation.Autowired;

import java.io.ByteArrayInputStream;
import java.util.List;

@ViewController("virtual-list-inline-editor")
@ViewDescriptor("virtual-list-inline-editor.xml")
public class VirtualListInlineEditorSample extends StandardView {

    @Autowired
    private Messages messages;
    @Autowired
    private DialogWindows dialogWindows;
    @Autowired
    private FoodPlaceholderDataGenerator foodPlaceholderDataGenerator;

    @ViewComponent
    private DataContext dataContext;
    @ViewComponent
    private CollectionContainer<Food> foodDc;

    @Supply(to = "foodList", subject = "renderer")
    public Renderer<Food> foodListRenderer() {
        return new ComponentRenderer<>(item -> {
            HorizontalLayout rootCardLayout = new HorizontalLayout();
            rootCardLayout.setMargin(true);

            VerticalLayout infoLayout = new VerticalLayout();
            infoLayout.setSpacing(false);
            infoLayout.setPadding(false);
            infoLayout.setWidth("30%");

            Avatar avatar = new Avatar();
            avatar.addThemeVariants(AvatarVariant.XLARGE);

            if (item.getIcon() != null && item.getIcon().length > 0) {
                String iconFileName = "%s.png".formatted(item.getTitle());
                InputStreamDownloadHandler handler = DownloadHandler.fromInputStream(event -> {
                    byte[] icon = item.getIcon();
                    ByteArrayInputStream inputStream = new ByteArrayInputStream(item.getIcon());

                    return new DownloadResponse(inputStream, iconFileName, "image/png", icon.length);
                });

                avatar.setImageHandler(handler);
            }

            VerticalLayout verticalLayout = new VerticalLayout();
            verticalLayout.setWidthFull();

            HorizontalLayout itemDetailLayout = new HorizontalLayout();
            itemDetailLayout.add(new Text(item.getDescription()));
            itemDetailLayout.add(new Html(
                    messages.formatMessage(getClass(), "foodListItemDescription", item.getPrice()))
            );
            itemDetailLayout.setPadding(false);
            itemDetailLayout.setAlignItems(FlexComponent.Alignment.CENTER);

            infoLayout.add(new Html(messages.formatMessage(getClass(), "foodItemTitle", item.getTitle())));
            infoLayout.add(itemDetailLayout);

            VerticalLayout buttonsPanel = new VerticalLayout();
            buttonsPanel.setWidth("AUTO");
            buttonsPanel.setPadding(false);
            buttonsPanel.setSpacing(false);

            Button detailButton = new Button(new Icon(VaadinIcon.PENCIL));
            detailButton.setText(messages.getMessage("actions.Edit"));
            detailButton.addClickListener(e -> dialogWindows.detail(this, Food.class)
                    .withViewClass(FoodDetailView.class)
                    .editEntity(item)
                    .withAfterCloseListener(closeEvent -> {
                        if (closeEvent.closedWith(StandardOutcome.SAVE)) {
                            foodDc.replaceItem(closeEvent.getSource().getView().getEditedEntity());
                        }
                    })
                    .open());
            detailButton.addClassName(StyleUtility.Button.LINK_BUTTON);

            Button removeButton = new Button(new Icon(VaadinIcon.TRASH));
            removeButton.setText(messages.getMessage("actions.Remove"));
            removeButton.addThemeVariants(ButtonVariant.ERROR);
            removeButton.addClassName(StyleUtility.Button.LINK_BUTTON);
            removeButton.addClickListener(e -> {
                foodDc.getMutableItems().remove(item);
                dataContext.remove(dataContext.merge(item));
            });

            buttonsPanel.add(detailButton, removeButton);
            rootCardLayout.add(avatar, infoLayout, buttonsPanel);
            return rootCardLayout;
        });
    }

    @Install(to = "foodDl", target = Target.DATA_LOADER)
    public List<Food> foodDlLoadDelegate(final LoadContext<Food> loadContext) {
        return foodPlaceholderDataGenerator.getFoodSamplesList();
    }

    @Subscribe(id = "addBtn", subject = "clickListener")
    public void onAddBtnClick(final ClickEvent<JmixButton> event) {
        dialogWindows.detail(this, Food.class)
                .withViewClass(FoodDetailView.class)
                .newEntity()
                .withAfterCloseListener(closeEvent -> {
                    if (closeEvent.closedWith(StandardOutcome.SAVE)) {
                        foodDc.replaceItem(closeEvent.getSource().getView().getEditedEntity());
                    }
                })
                .open();
    }
}




Food.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.annotation.Nullable;
import jakarta.persistence.Id;
import jakarta.validation.constraints.NotNull;

import java.util.UUID;

@JmixEntity
public class Food {
    @JmixGeneratedValue
    @Id
    private UUID id;

    @NotNull
    @InstanceName
    private String title;

    @NotNull
    private Integer price;

    @Nullable
    private String description;

    @Nullable
    private byte[] icon;

    @Nullable
    public byte[] getIcon() {
        return icon;
    }

    public void setIcon(byte[] icon) {
        this.icon = icon;
    }

    public Integer getPrice() {
        return price;
    }

    public void setPrice(Integer price) {
        this.price = price;
    }

    @Nullable
    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }
}




FoodDetailView.java

package io.jmix.uisamples.view.entity.food;


import com.vaadin.flow.component.avatar.Avatar;
import com.vaadin.flow.component.html.H2;
import com.vaadin.flow.server.streams.DownloadHandler;
import com.vaadin.flow.server.streams.DownloadResponse;
import com.vaadin.flow.server.streams.InputStreamDownloadHandler;
import io.jmix.flowui.component.SupportsTypedValue.TypedValueChangeEvent;
import io.jmix.flowui.component.textfield.TypedTextField;
import io.jmix.flowui.component.upload.FileUploadField;
import io.jmix.flowui.model.InstanceContainer;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Food;
import org.apache.commons.lang3.StringUtils;

import java.io.ByteArrayInputStream;

@DialogMode(minWidth = "15em", minHeight = "10pm")
@EditedEntityContainer("foodDc")
@ViewController("Food.detail")
@ViewDescriptor("food-detail-view.xml")
public class FoodDetailView extends StandardDetailView<Food> {

    @ViewComponent
    private Avatar foodIcon;
    @ViewComponent
    private FileUploadField foodIconUpload;
    @ViewComponent
    private H2 foodTitle;

    @Subscribe
    public void onBeforeShow(final BeforeShowEvent event) {
        initIconComponents();
    }

    @Subscribe("titleField")
    public void onNameFieldTypedValueChange(final TypedValueChangeEvent<TypedTextField<String>, String> event) {
        foodTitle.setText(event.getValue());
    }

    @Subscribe(id = "foodDc", target = Target.DATA_CONTAINER)
    protected void onPropertyChangeListener(InstanceContainer.ItemPropertyChangeEvent<Food> event) {
        if ("icon".equals(event.getProperty())) {
            initIconComponents();
        }
    }

    private void initIconComponents() {
        if (StringUtils.isNotBlank(getEditedEntity().getTitle())) {
            foodTitle.setText(getEditedEntity().getTitle());
        }
        byte[] iconArray = getEditedEntity().getIcon();
        if (iconArray != null && iconArray.length > 0) {
            try {
                String iconFileName = "%s.png".formatted(getEditedEntity().getTitle());
                InputStreamDownloadHandler handler = DownloadHandler.fromInputStream(event -> {
                    byte[] icon = getEditedEntity().getIcon();
                    ByteArrayInputStream inputStream = new ByteArrayInputStream(getEditedEntity().getIcon());

                    return new DownloadResponse(inputStream, iconFileName, "image/png", icon.length);
                });

                foodIcon.setImageHandler(handler);
                foodIconUpload.setValue(iconArray);
            } catch (RuntimeException e) {
                throw new RuntimeException("Cannot init fields on food", e);
            }
        }
    }
}




food-detail-view.xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<view xmlns="http://jmix.io/schema/flowui/view"
      title="msg://FoodDetailView.title">
    <data>
        <instance id="foodDc" class="io.jmix.uisamples.entity.Food"/>
    </data>
    <actions>
        <action id="saveAction" type="detail_saveClose"/>
        <action id="closeAction" type="detail_close"/>
    </actions>
    <layout>
        <hbox>
            <h2 id="foodTitle"/>
            <avatar id="foodIcon" />
            <fileUploadField id="foodIconUpload" dataContainer="foodDc" property="icon" uploadIcon="UPLOAD" uploadText=""/>
        </hbox>
        <formLayout id="form" dataContainer="foodDc">
            <textField id="titleField" property="title"/>
            <textField property="description"/>
            <textField property="price">
                <validators>
                    <positive message="msg://price.validation.negative"/>
                </validators>
            </textField>
        </formLayout>
        <hbox id="detailActions">
            <button id="saveAndCloseBtn" action="saveAction"/>
            <button id="closeBtn" action="closeAction"/>
        </hbox>
    </layout>
</view>



FoodPlaceholderDataGenerator.java

package io.jmix.uisamples.bean;

import io.jmix.core.Messages;
import io.jmix.core.Metadata;
import io.jmix.core.Resources;
import io.jmix.uisamples.entity.Food;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

@Component("uisamples_FoodPlaceholderDataGenerator")
public class FoodPlaceholderDataGenerator {
    private static final String NOOP_DESCRIPTION = "";

    @Autowired
    private Metadata metadata;
    @Autowired
    private Messages messages;
    @Autowired
    private Resources resources;

    public List<Food> getFoodSamplesList() {
        List<Food> foodList = new ArrayList<>();
        foodList.add(createFoodSample(messages.getMessage(getClass(), "sample.food.burger.title"),
                messages.getMessage(getClass(), "sample.food.burger.description"),
                7, "META-INF/resources/icons/components/virtuallist-food/burger.png"));

        foodList.add(createFoodSample(messages.getMessage(getClass(), "sample.food.cola.title"),
                messages.getMessage(getClass(), "sample.food.cola.description"),
                4, "META-INF/resources/icons/components/virtuallist-food/cola.png"));

        foodList.add(createFoodSample(messages.getMessage(getClass(), "sample.food.fries.title"),
                messages.getMessage(getClass(), "sample.food.fries.description"),
                3, "META-INF/resources/icons/components/virtuallist-food/fries.png"));

        foodList.add(createFoodSample(messages.getMessage(getClass(), "sample.food.pizza.title"),
                messages.getMessage(getClass(), "sample.food.pizza.description"),
                15, "META-INF/resources/icons/components/virtuallist-food/pizza.png"));

        foodList.add(createFoodSample(messages.getMessage(getClass(), "sample.food.sandwich.title"),
                NOOP_DESCRIPTION,
                2, "META-INF/resources/icons/components/virtuallist-food/sandwich.png"));
        return foodList;
    }

    private Food createFoodSample(String title,
                                  String description,
                                  int price,
                                  String iconLocation) {
        Food food = metadata.create(Food.class);
        food.setTitle(title);
        food.setDescription(description);
        food.setPrice(price);
        try (InputStream imageStream = resources.getResourceAsStream(iconLocation)) {
            food.setIcon(Objects.requireNonNull(imageStream).readAllBytes());
        } catch (IOException e) {
            throw new RuntimeException("Cannot open a stream", e);
        }
        return food;
    }
}


