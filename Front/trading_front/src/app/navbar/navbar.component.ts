import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common'; // Importer CommonModule pour ngFor

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css'
})
export class NavbarComponent {
  markets = [
    { name: 'Marché 1', id: 1 },
    { name: 'Marché 2', id: 2 },
    { name: 'Marché 3', id: 3 },
    // Ajoutez d'autres marchés ici
  ];
  
  selectedMarket: string = this.markets[0].name; // Valeur par défaut
  price: number = 0; // Prix initial

  buy() {
    alert(`Achat de ${this.selectedMarket} au prix de ${this.price}`);
    // Ajoutez ici la logique pour traiter l'achat
  }

  sell() {
    alert(`Vente de ${this.selectedMarket} au prix de ${this.price}`);
    // Ajoutez ici la logique pour traiter la vente
  }
}
