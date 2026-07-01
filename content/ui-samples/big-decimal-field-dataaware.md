<Path>Components > BigDecimalField > Data-aware BigDecimalField</Path>

The dataContainer and property attributes are used to connect the BigDecimalField to an entity attribute. The dataContainer contains an entity instance; property specifies an attribute to edit.

big-decimal-field-dataaware.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <data>
        <instance id="productDc"
                  class="io.jmix.uisamples.entity.Product"
                  fetchPlan="_local"/>
    </data>
    <layout>
        <bigDecimalField id="bigDecimalField" label="Field connected to a container" width="15em"
                         dataContainer="productDc" property="price"/>
        <hbox>
            <span text="Value in the container:"/>
            <span id="spanValue"/>
        </hbox>
    </layout>
</view>




BigDecimalFieldDataawareSample.java

package io.jmix.uisamples.view.flowui.components.bigdecimalfield.dataaware;

import com.vaadin.flow.component.AbstractField.ComponentValueChangeEvent;
import com.vaadin.flow.component.html.Span;
import io.jmix.core.Metadata;
import io.jmix.flowui.component.textfield.JmixBigDecimalField;
import io.jmix.flowui.model.InstanceContainer;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Product;
import org.springframework.beans.factory.annotation.Autowired;

import java.math.BigDecimal;

@ViewController("big-decimal-field-dataaware")
@ViewDescriptor("big-decimal-field-dataaware.xml")
public class BigDecimalFieldDataawareSample extends StandardView {

    @ViewComponent
    protected InstanceContainer<Product> productDc;
    @ViewComponent
    protected Span spanValue;

    @Autowired
    protected Metadata metadata;

    @Subscribe
    protected void onInit(InitEvent event) {
        Product product = metadata.create(Product.class);
        product.setPrice(BigDecimal.TEN);
        productDc.setItem(product);
    }

    @Subscribe("bigDecimalField")
    protected void onBigDecimalFieldValueChange(ComponentValueChangeEvent<JmixBigDecimalField, BigDecimal> changeEvent) {
        BigDecimal price = productDc.getItem().getPrice();
        spanValue.setText(price == null ? "null" : price.toString());
    }
}




Product.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.*;

import java.math.BigDecimal;
import java.util.List;
import java.util.UUID;

@Table(name = "PRODUCT")
@Entity
@JmixEntity
public class Product {

    @Id
    @Column(name = "ID", nullable = false)
    @JmixGeneratedValue
    protected UUID id;

    @Column(name = "NAME", nullable = false)
    @InstanceName
    protected String name;

    @Column(name = "PRICE", nullable = false)
    protected BigDecimal price;

    @JoinTable(name = "PRODUCT_PRODUCT_TAG_LINK",
            joinColumns = @JoinColumn(name = "PRODUCT_ID"),
            inverseJoinColumns = @JoinColumn(name = "PRODUCT_TAG_ID"))
    @ManyToMany
    private List<ProductTag> tags;

    public Product() {
        this.id = UUID.randomUUID();
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public void setPrice(BigDecimal price) {
        this.price = price;
    }

    public BigDecimal getPrice() {
        return price;
    }

    public List<ProductTag> getTags() {
        return tags;
    }

    public void setTags(List<ProductTag> tags) {
        this.tags = tags;
    }
}


