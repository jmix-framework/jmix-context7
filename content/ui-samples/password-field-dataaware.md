<Path>Components > PasswordField > Data-aware PasswordField</Path>

The dataContainer and property attributes are used to connect the PasswordField to an entity attribute. The dataContainer contains an entity instance; property specifies an attribute to edit.

password-field-dataaware.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <data>
        <instance id="productTagDc"
                  class="io.jmix.uisamples.entity.ProductTag"
                  fetchPlan="_local"/>
    </data>
    <layout>
        <passwordField id="passwordField" label="Field connected to a container" width="15em"
                         dataContainer="productTagDc" property="name"/>
        <hbox>
            <span text="Value in the container:"/>
            <span id="spanValue"/>
        </hbox>
    </layout>
</view>




PasswordFieldDataawareSample.java

package io.jmix.uisamples.view.flowui.components.passwordfield.dataaware;

import com.vaadin.flow.component.AbstractField.ComponentValueChangeEvent;
import com.vaadin.flow.component.html.Span;
import com.vaadin.flow.component.textfield.PasswordField;
import io.jmix.core.Metadata;
import io.jmix.flowui.model.InstanceContainer;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.ProductTag;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("password-field-dataaware")
@ViewDescriptor("password-field-dataaware.xml")
public class PasswordFieldDataawareSample extends StandardView {

    @ViewComponent
    protected InstanceContainer<ProductTag> productTagDc;
    @ViewComponent
    protected Span spanValue;

    @Autowired
    protected Metadata metadata;

    @Subscribe
    protected void onInit(InitEvent event) {
        ProductTag productTag = metadata.create(ProductTag.class);
        productTag.setName("Secret name");
        productTagDc.setItem(productTag);
    }

    @Subscribe("passwordField")
    protected void onPasswordFieldValueChange(ComponentValueChangeEvent<PasswordField, String> changeEvent) {
        spanValue.setText(productTagDc.getItem().getName());
    }
}




ProductTag.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.DependsOnProperties;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

import java.util.UUID;

@JmixEntity
@Table(name = "PRODUCT_TAG")
@Entity
public class ProductTag {

    @JmixGeneratedValue
    @Column(name = "ID", nullable = false)
    @Id
    private UUID id;

    @Column(name = "NAME")
    private String name;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    @InstanceName
    @DependsOnProperties({"name"})
    public String getInstanceName() {
        return String.format("%s", name);
    }
}

