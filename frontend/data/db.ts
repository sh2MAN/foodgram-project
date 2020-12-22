export interface User {
    id: number;
    login: string;
    email: string;
    password: string;
}

export interface Tags {
    name: string;
}

export interface Receip {
    author: User;
    title: string;
    image: ImageData;
    text: Text;
    tag: Tags;
    time: number;
    slug: string;
}

export interface Receip_Ingredients {
    receip_id: Receip;
    ingredients_id: Ingredients;
}

export interface Ingredients {
    name: string;
    weight: MeasureUnit;
}

export interface MeasureUnit {
    name: string;
}

export interface Follow {
    user: User;
    author: User;
}

export interface Favorite {
    user: User;
    receip: Receip;
}